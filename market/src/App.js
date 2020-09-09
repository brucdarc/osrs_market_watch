import React from 'react';
import logo from './logo.svg';
import './App.css';
import Image from 'react-bootstrap/Image'
import { Container, Row, Grid } from 'react-bootstrap';

function App() {
  return (
    <div>
    <div className="App">
      <header className="App-header">
        <Image src="https://oldschool.runescape.wiki/images/6/63/Coins_detail.png?404bc"/>
        <form>
          <label>
            Name:
            <input type="text" name="name" />
          </label>
          <input type="submit" value="Submit" />
        </form>
      </header>
    </div>
    <div>
        <Grid>
          <Row>
            <Col>1 of 2</Col>
            <Col>2 of 2</Col>
          </Row>
          <Row>
            <Col>1 of 3</Col>
            <Col>2 of 3</Col>
            <Col>3 of 3</Col>
          </Row>
        </Grid>
    </div>
    </div>
  );
}

export default App;
