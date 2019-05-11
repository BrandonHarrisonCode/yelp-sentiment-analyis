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
          <p className="material-icons" style={{color: "yellow"}} onClick={this.toggle}>
            <Restaurant/>
            <div style={{color: 'white', fontSize: '.8em', position: 'relative', right: '2px'}}>{this.props.restaurant['restaurant_name']}</div>
          </p>
        </div>

        <Modal scrollable isOpen={this.state.modal} toggle={this.toggle} className={this.props.className} centered = "true">
          <ModalHeader
            toggle={this.toggle}>
              <font size="5">{this.props.restaurant['restaurant_name']}</font><br />
              <font size="3">Top 10 Dishes</font>
          </ModalHeader>
          <ModalBody>
          {Object.keys(this.props.restaurant['dishes']).map((index) => {
            var rank = parseInt(index, 10) + 1;
            if (rank > 10) {
              return ''
            }
            return <p>{rank}: {this.props.restaurant['dishes'][index]}</p>
            }
          )}
          </ModalBody>
          <ModalFooter>
            <Button color="secondary" onClick={this.toggle}>Close</Button>
          </ModalFooter>
        </Modal>
      </div>
    );
  }
}

export default Place;
