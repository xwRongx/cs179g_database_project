var express = require('express');
var router = express.Router();
var db = require('../database');

// GET /api/health. The frontend can use this route to check if MySQL is available
router.get('/health', async function(req, res) {
  try {
    await db.query('SELECT 1');
    res.json({ database: 'connected' });
  } catch (error) {
    console.error('Database health check failed:', error.message);
    res.status(503).json({
      database: 'disconnected',
      error: 'Could not connect to MySQL. Check the database settings.'
    });
  }
});

// Returns one point per year for a line chart
router.get('/trends', async function(req, res) {
  var keyword = (req.query.keyword || '').trim();
  var startYear = req.query.startYear;
  var endYear = req.query.endYear;

  if (!keyword) {
    return res.status(400).json({ error: 'The keyword query parameter is required.' });
  }

  if (keyword.length > 255) {
    return res.status(400).json({ error: 'The keyword must be 255 characters or fewer.' });
  }

  if (startYear !== undefined && !isValidYear(startYear)) {
    return res.status(400).json({ error: 'startYear must be a valid year.' });
  }

  if (endYear !== undefined && !isValidYear(endYear)) {
    return res.status(400).json({ error: 'endYear must be a valid year.' });
  }

  if (startYear !== undefined && endYear !== undefined && Number(startYear) > Number(endYear)) {
    return res.status(400).json({ error: 'startYear cannot be after endYear.' });
  }

  var sql = `
    SELECT year, SUM(match_count) AS match_count
    FROM word_year_stats
    WHERE LOWER(word) = LOWER(?)
  `;

  var values = [keyword];

  if (startYear !== undefined) {
    sql += ' AND year >= ?';
    values.push(Number(startYear));
  }

  if (endYear !== undefined) {
    sql += ' AND year <= ?';
    values.push(Number(endYear));
  }

  sql += ' GROUP BY year ORDER BY year ASC';

  try {
    var [rows] = await db.query(sql, values);

    res.json({
      keyword: keyword,
      data: rows.map(function(row) {
        return {
          year: Number(row.year),
          match_count: Number(row.match_count)
        };
      })
    });
  } catch (error) {
    sendDatabaseError(res, error);
  }
});

// Returns the decades that can be shown in a frontend dropdown
router.get('/decades', async function(req, res) {
  try {
    var [rows] = await db.query(
      'SELECT DISTINCT decade FROM decade_top_words ORDER BY decade ASC'
    );

    res.json({
      data: rows.map(function(row) {
        return Number(row.decade);
      })
    });
  } catch (error) {
    sendDatabaseError(res, error);
  }
});

// Returns ranked words that can be used in a bar chart
router.get('/top-words', async function(req, res) {
  var decade = req.query.decade;
  var limit = req.query.limit === undefined ? 10 : Number(req.query.limit);

  var ranking = req.query.ranking || 'top';
  var removeStopWords = req.query.removeStopWords === 'true';
  var dictionaryOnly = req.query.dictionaryOnly === 'true';

  if (!isValidDecade(decade)) {
    return res.status(400).json({
      error: 'decade is required and must be a year ending in 0, such as 1990.'
    });
  }

  if (!Number.isInteger(limit) || limit < 1 || limit > 50) {
    return res.status(400).json({
      error: 'limit must be a whole number from 1 to 50.'
    });
  }

  if (ranking !== 'top' && ranking !== 'bottom') {
    return res.status(400).json({
      error: 'ranking must be top or bottom.'
    });
  }

  var table;

  if (ranking === 'top') {
    if (removeStopWords) {
      table = 'decade_top_words_no_stop';
    } else {
      table = 'decade_top_words';
    }
  } else {
    if (dictionaryOnly) {
      table = 'decade_bottom_words_dictionary';
    } else {
      table = 'decade_bottom_words';
    }
  }

  try {
    var [rows] = await db.query(
      `SELECT word, total_matches, word_rank
       FROM ${table}
       WHERE decade = ?
       ORDER BY word_rank ASC
       LIMIT ?`,
      [Number(decade), limit]
    );

    res.json({
      decade: Number(decade),
      data: rows.map(function(row) {
        return {
          word: row.word,
          total_matches: Number(row.total_matches),
          rank: Number(row.word_rank)
        };
      })
    });
  } catch (error) {
    sendDatabaseError(res, error);
  }
});

// Returns the top or bottom word for each year in a 10 year period
router.get('/top-words-year', async function(req, res) {
  var year = req.query.year;
  var ranking = req.query.ranking || 'top';
  var removeStopWords = req.query.removeStopWords === 'true';
  var dictionaryOnly = req.query.dictionaryOnly === 'true';

  if (!isValidYear(year)) {
    return res.status(400).json({
      error: 'year must be a valid year.'
    });
  }

  if (ranking !== 'top' && ranking !== 'bottom') {
    return res.status(400).json({
      error: 'ranking must be top or bottom.'
    });
  }

  var table;

  if (ranking === 'top') {
    if (removeStopWords) {
      table = 'top_word_year_no_stop';
    } else {
      table = 'top_word_year';
    }
  } else {
    if (dictionaryOnly) {
      table = 'bottom_word_year_dictionary';
    } else {
      table = 'bottom_word_year';
    }
  }

  var endYear = Number(year) + 9;

  try {
    var [rows] = await db.query(
      `SELECT year, word, total_matches
       FROM ${table}
       WHERE year BETWEEN ? AND ?
       ORDER BY year ASC`,
      [Number(year), endYear]
    );

    res.json({
      data: rows.map(function(row) {
        return {
          year: Number(row.year),
          word: row.word,
          total_matches: Number(row.total_matches)
        };
      })
    });
  } catch (error) {
    sendDatabaseError(res, error);
  }
});

function isValidYear(value) {
  var year = Number(value);
  return Number.isInteger(year) && year >= 1500 && year <= 2100;
}

function isValidDecade(value) {
  return isValidYear(value) && Number(value) % 10 === 0;
}

function sendDatabaseError(res, error) {
  console.error('Database query failed:', error.message);
  res.status(500).json({
    error: 'The database query failed. Check that MySQL is running and the Part 2 tables are loaded.'
  });
}

module.exports = router;