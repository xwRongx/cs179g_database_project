import { useState } from 'react';
import './App.css';

import TopYear from './TopYear';
import TopDecade from './TopDecade';

function App() {
  const [entered, setEntered] = useState(false);

  if (!entered) {
    return (
      <div className="landing-page">
        <div className="landing-card">

          <p className="eyebrow">
            CS179G Project
          </p>

          <h1>
            Word Trends
          </h1>

          <p className="landing-description">
            Group 3
          </p>

          <button
            className="primary-button"
            onClick={() => setEntered(true)}
          >
            Enter
          </button>

        </div>
      </div>
    );
  }

  return <Dashboard />;
}


function Dashboard() {

  const [graphType, setGraphType] = useState('decade');

  const [ranking, setRanking] = useState('top');

  const [removeStopWords, setRemoveStopWords] = useState(false);

  const [dictionaryOnly, setDictionaryOnly] = useState(false);

  const [searchWord, setSearchWord] = useState('');


  function handleSearch(event) {
    event.preventDefault();

    console.log('Search word:', searchWord);
  }


  function selectTop() {
    setRanking('top');

    // Dictionary filtering is only used
    // for bottom-word data.
    setDictionaryOnly(false);
  }


  function selectBottom() {
    setRanking('bottom');

    // Stop-word filtering is only used
    // for top-word data.
    setRemoveStopWords(false);
  }


  return (
    <div className="dashboard">

      {/* Header */}

      <header className="page-header">

        <div>

          <p className="eyebrow">
            CS179G Project
          </p>

          <h1>
            Word Trends
          </h1>

        </div>

      </header>


      <main className="dashboard-content">

        {/* Top Controls */}

        <section className="toolbar-card">

          {/* Search */}

          <form
            className="search-form"
            onSubmit={handleSearch}
          >

            <label htmlFor="word-search">
              Search for a word
            </label>


            <div className="search-row">

              <input
                id="word-search"
                type="text"
                placeholder="e.g. computer"
                value={searchWord}
                onChange={(event) =>
                  setSearchWord(event.target.value)
                }
              />


              <button
                className="primary-button"
                type="submit"
              >
                Search
              </button>

            </div>

          </form>


          {/* Graph Type */}

          <div className="graph-switcher">

            <span className="control-label">
              Display
            </span>


            <button
              type="button"
              className={
                graphType === 'decade'
                  ? 'tab active'
                  : 'tab'
              }
              onClick={() =>
                setGraphType('decade')
              }
            >
              Words by Decade
            </button>


            <button
              type="button"
              className={
                graphType === 'year'
                  ? 'tab active'
                  : 'tab'
              }
              onClick={() =>
                setGraphType('year')
              }
            >
              Words by Year
            </button>

          </div>


          {/* Top / Bottom */}

          <div className="graph-switcher">

            <span className="control-label">
              Ranking
            </span>


            <button
              type="button"
              className={
                ranking === 'top'
                  ? 'tab active'
                  : 'tab'
              }
              onClick={selectTop}
            >
              Top
            </button>


            <button
              type="button"
              className={
                ranking === 'bottom'
                  ? 'tab active'
                  : 'tab'
              }
              onClick={selectBottom}
            >
              Bottom
            </button>

          </div>

        </section>


        {/* Visualization */}

        <section className="visualization-layout">


          {/* Graph */}

          <div className="graph-card">

            <div className="graph-card-header">

              <div>

                <p className="section-label">
                  Visualization
                </p>


                <h2>

                  {ranking === 'top'
                    ? 'Top '
                    : 'Bottom '}

                  {graphType === 'decade'
                    ? 'Words by Decade'
                    : 'Words by Year'}

                </h2>

              </div>

            </div>


            <div className="graph-component">

              {graphType === 'decade'
                ? (
                    <TopDecade
                      ranking={ranking}
                      removeStopWords={removeStopWords}
                      dictionaryOnly={dictionaryOnly}
                    />
                  )
                : (
                    <TopYear
                      ranking={ranking}
                      removeStopWords={removeStopWords}
                      dictionaryOnly={dictionaryOnly}
                    />
                  )
              }

            </div>

          </div>


          {/* Filters */}

          <aside className="filter-card">

            <p className="section-label">
              Filters
            </p>


            {/* Stop Words */}

            <label className="checkbox-row">

              <input
                type="checkbox"
                checked={removeStopWords}
                disabled={ranking === 'bottom'}
                onChange={(event) =>
                  setRemoveStopWords(
                    event.target.checked
                  )
                }
              />

              <span>
                Remove stop words
              </span>

            </label>


            {/* Dictionary Words */}

            <label className="checkbox-row">

              <input
                type="checkbox"
                checked={dictionaryOnly}
                disabled={ranking === 'top'}
                onChange={(event) =>
                  setDictionaryOnly(
                    event.target.checked
                  )
                }
              />

              <span>
                Dictionary words only
              </span>

            </label>


            {/* Filter Explanation */}

            {ranking === 'top'
              ? (
                  <p className="filter-note">
                    Stop-word filtering is available
                    for top-word results.
                  </p>
                )
              : (
                  <p className="filter-note">
                    Dictionary filtering is available
                    for bottom-word results.
                  </p>
                )
            }

          </aside>

        </section>

      </main>

    </div>
  );
}


export default App;