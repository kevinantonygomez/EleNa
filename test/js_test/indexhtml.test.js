const { JSDOM } = require('jsdom');

describe('HTML structure and content', () => {
  let dom;
  let document;

  beforeEach(() => {
    const htmlContent = `
      <!DOCTYPE html>
      <html lang="en" dir="ltr">
        <head>
          <meta charset="utf-8">
          <title>EleNa</title>
          <link rel="stylesheet" href="css/indexStyle.css">
          <link rel="stylesheet" href="https://js.arcgis.com/4.26/esri/themes/light/main.css">
          <script src="https://js.arcgis.com/4.26/"></script>
          <script src="js/indexScript.js" async></script>
          <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        </head>
        <body>
          <div class="container">
            <div id="modal">
              <div id="modal-content">
                <span id="close-modal">&times;</span>
                <p>Used to specify the maximum distance over the shortest possible route that the user is willing to travel. The generated routes are strictly within this threshold.</p>
              </div>
            </div>
            <div id="controls-div">
              <div id="logo-div">
                <img src="img/temporaryLogo.png" alt="EleNa Logo", id="logo">
              </div>
              <div id="transport-select-div">
                <button type="button" id="drive" class="inactiveRoute" title="Driving"></button>
                <button type="button" id="walk" class="inactiveRoute" title="Walking"></button>
                <button type="button" id="bike" class="inactiveRoute" title="Cycling"></button>
              </div>
              <div id="address-parent-div">
                <div id="address-div">
                  <div id="start-search-div"></div>
                  <div id="stop-search-div"></div>
                </div>
                <div id="address-swap-div">
                  <button type="button" id="swap-btn" title="Reverse starting point and destination">↑↓</button>
                </div>
              </div>
              <div id="params-div">
                <div id="elevation-algorithm-div">
                  <div id="elevation-div">
                    <fieldset>
                      <legend>Elevation Gain</legend>
                      <div>
                        <input type="radio" id="max-gain" name="gain-radio" value="maximize" checked>
                        <label for="maximize">Maximize</label>
                      </div>
                      <div>
                        <input type="radio" id="min-gain" name="gain-radio" value="minimize">
                        <label for="minimize">Minimize</label>
                      </div>
                    </fieldset>
                  </div>
                  <div>
                    <fieldset>
                      <legend>Algorithm</legend>
                      <div>
                        <input type="radio" id="a-star" name="alg-radio" value="A*" checked>
                        <label for="A*">A*</label>
                      </div>
                      <div>
                        <input type="radio" id="dijkstra" name="alg-radio" value="dijkstra">
                        <label for="Dijkstra">Dijkstra</label>
                      </div>
                    </fieldset>
                  </div>
                </div>
                <div id="distance-info-div">
                  <div>
                    <fieldset>
                      <legend>Max Distance (%)</legend>
                      <div id="distance-div">
                        <input type="number" id="distance-input" min="0" max="100" step="0.5" value="0">
                      </div>
                    </fieldset>
                  </div>
                  <div id="info-button-div">
                    <button type="button" id="info-btn" title="info">i</button>
                  </div>
                </div>
              </div>
              <div id="go-button-div">
                <button type="button" id="go-btn">GO</button>
              </div>
            </div>
            <div id="map-div"></div>
          </div>
        </body>
      </html>
    `;

    dom = new JSDOM(htmlContent);
    document = dom.window.document;
  });

  it('Webpage should have a title', () => {
    expect(document.querySelector('title').textContent).toBe('EleNa');
  });

  it('Webpage should have CSS and JavaScript dependencies', () => {
    expect(document.querySelector('link[href="css/indexStyle.css"]')).toBeTruthy();
    expect(document.querySelector('link[href="https://js.arcgis.com/4.26/esri/themes/light/main.css"]')).toBeTruthy();
    expect(document.querySelector('script[src="https://js.arcgis.com/4.26/"]')).toBeTruthy();
    expect(document.querySelector('script[src="js/indexScript.js"][async]')).toBeTruthy();
    expect(document.querySelector('script[src="https://code.jquery.com/jquery-3.6.0.min.js"]')).toBeTruthy();
  });

  it('Container div should have specific elements', () => {
    const container = document.querySelector('.container');

    expect(container.querySelector('#modal')).toBeTruthy();
    expect(container.querySelector('#controls-div')).toBeTruthy();
    expect(container.querySelector('map-div'));
  });

  it('Modal div should have specific elements', () => {
    const modal = document.querySelector('#modal');

    expect(modal.querySelector('#modal-content')).toBeTruthy();
    expect(modal.querySelector('#close-modal')).toBeTruthy();
  });

  it('Controls div should have specific elements', () => {
    const controls = document.querySelector('#controls-div');

    expect(controls.querySelector('#logo-div')).toBeTruthy();
    expect(controls.querySelector('#logo')).toBeTruthy();
    expect(controls.querySelector('#transport-select-div')).toBeTruthy();
    expect(controls.querySelector('#drive')).toBeTruthy();
    expect(controls.querySelector('#bike')).toBeTruthy();
    expect(controls.querySelector('#walk')).toBeTruthy();
    expect(controls.querySelector('#address-parent-div')).toBeTruthy();
    expect(controls.querySelector('#address-div')).toBeTruthy();
    expect(controls.querySelector('#start-search-div')).toBeTruthy();
    expect(controls.querySelector('#stop-search-div')).toBeTruthy();
    expect(controls.querySelector('#address-swap-div')).toBeTruthy();
    expect(controls.querySelector('#swap-btn')).toBeTruthy();
    expect(controls.querySelector('#params-div')).toBeTruthy();
    expect(controls.querySelector('#elevation-algorithm-div')).toBeTruthy();
    expect(controls.querySelector('#distance-info-div')).toBeTruthy();
    expect(controls.querySelector('#go-button-div')).toBeTruthy();

    const transportSelectDiv = document.querySelector('.container').querySelector('#transport-select-div');
    expect(transportSelectDiv.querySelectorAll('button')).toHaveLength(3);

  });

  it('Logo should be rendered', () => {
    const logoImg = document.querySelector('#logo');
    expect(logoImg).toBeTruthy();
    expect(logoImg.getAttribute('src')).toBe('img/temporaryLogo.png');
    expect(logoImg.getAttribute('alt')).toBe('EleNa Logo');
  });

});
