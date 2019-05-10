import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import Restaurant from '@material-ui/icons/Restaurant'

class Place extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      modal: false
    };

    this.toggle = this.toggle.bind(this);
  }

  toggle() {
    this.setState(prevState => ({
      modal: !prevState.modal
    }));
  }

   render() {
    return (
      <div>
        <div className="icon" >
          <p className="material-icons" style={{color: "#93C054"}} onClick={this.toggle}>
            <Restaurant/>
            <div style={{color: 'white', fontSize: '.8em', position: 'relative', right: '2px'}}>{this.props.restaurant['restaurant_name']}</div>
          </p>
        </div>

        <Modal scrollable isOpen={this.state.modal} toggle={this.toggle} className={this.props.className} centered = "true">
          <ModalHeader
            toggle={this.toggle}>
              <font size="5">{this.props.restaurant['restaurant_name']}</font><br />
          </ModalHeader>
          <ModalBody>

          </ModalBody>
          <ModalFooter>
            <Button color="secondary" onClick={this.toggle}>Cancel</Button>
          </ModalFooter>
        </Modal>
      </div>
    );
  }
}

export default Place;

//Harvest Start: {this.props.plantInfoProp['Harvest Start']} <br />
//Harvest End: {this.props.plantInfoProp['Harvest End']} <br />
//<hr color = "black" width = "90%"></hr>
//Fruit Edibility: {this.displayTF(this.props.plantInfoProp['Edible (fruit) Y/N'])} <br />
//Flower Edibility: {this.displayTF(this.props.plantInfoProp['Edible Flower  Y/N'])} <br />
//Leaf Edibility: {this.displayTF(this.props.plantInfoProp['Edible Leaf'])} <br />
//Bark Edibility: {this.displayTF(this.props.plantInfoProp['Edible Bark Y/N'])} <br />
//Seed Edibility: {this.displayTF(this.props.plantInfoProp['Edible Seed'])} <br />
//Overall Toxicity Rating (1-4): {this.props.plantInfoProp['Toxicity (Rating: 1-4)']} <br />
//Fruit Type: {this.props.plantInfoProp['Fruit Type']} <br />
//Fruit Size: {this.props.plantInfoProp['Fruit Size']} <br />
//Bloom Color: {this.props.plantInfoProp['Bloom Color']} <br />
//Water Use: {this.props.plantInfoProp['Water Use']} <br />
//Planting Year: {this.props.plantInfoProp['Planting Year']}<br />
//Source: {this.props.plantInfoProp['Source']}
