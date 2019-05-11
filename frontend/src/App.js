import React, { Component } from 'react';
import './App.css';
import Place from './Place.js';
import GoogleMapReact from 'google-map-react';
import fetch from "node-fetch";

class App extends Component {

  constructor() {
    super()
    this.state = {
      places: [],
      center: {
        lat: 30.2532,
        lng: -97.7353
      },
      zoom: 10
    }
  }

  getJSON(url) {
    return fetch(url).then(response => {
      return response.json();
    });
  }

  componentDidMount() {
    this.getJSON("https://localhost:5000").then(response => {
      this.setState({places: JSON.parse(JSON.stringify(response))});
    });
  }

  render() {
    if (Object.keys(this.state.places).length === 0) {
      return (<p>Loading...</p>);
    }
    else {
      const places = this.state.places;
      return (
        <div className="App">
          <header className="App-header">
            <div style={{ height: '100vh', width: '100%' }}>
              <GoogleMapReact
                boostrapURLKeys={{key: 'AIzaSyBebQliWhp3IzIBvWa-svqC1xPuVAajJ5Q'}}
                defaultCenter={this.state.center}
                defaultZoom={this.state.zoom}
                >
                {Object.keys(places).map((index) => {
                  return <Place
                    restaurant={places[index]}
                    lat={places[index]['lat']}
                    lng={places[index]['lng']}
                  />
                  }
                )}
              </GoogleMapReact>
            </div>
          </header>
        </div>
      );
    }
  }
}

export default App;
