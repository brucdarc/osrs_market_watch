import React from 'react';
import logo from './logo.svg';
import Image from 'react-bootstrap/Image'
import { Container, Row, Col, Jumbotron } from 'reactstrap';
import Button from "@material-ui/core/Button";
import Thing from './Thing';

function App() {
  return (
    <div className="App">
      <Thing />
    </div>
  );
}

export default App;
