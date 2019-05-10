import React, { Component } from 'react';
import './App.css';
import Place from './Place.js';
import GoogleMapReact from 'google-map-react';

class App extends Component {

  constructor() {
    super()
    this.state = {
      places: [{restaurant_name: 'Test1', lat: 30.2535, lng: -97.732, dishes: []}, {restaurant_name: 'Test2', lat: 30.2544, lng: -97.710, dishes: []}],
      center: {
        lat: 30.2532,
        lng: -97.7353
      },
      zoom: 10
    }
  }

  componentDidMount() {
    // fetch('places.json')
    //   .then(response => response.json())
    //   .then((data) => {
    //     data.results.forEach((result) => {
    //       result.show = false; // eslint-disable-line no-param-reassign
    //     });
    //     this.setState({ places: data.results });
    //   });
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
                boostrapURLKeys={{key: process.env.REACT_APP_MAP_KEY}}
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

//defaultCenter={this.state.center}
//defaultZoom={this.state.zoom}
//options={function (maps) { return { mapTypeId: "satellite", minZoom: 19, maxZoom: 20, restriction: {
//  latLngBounds: {
//    east: -97.734,
//    north: 30.2535,
//    south: 30.2525,
//    west: -97.736
//  },
//  strictBounds: true
//}}}}
