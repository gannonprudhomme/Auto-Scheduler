// Contains the main content of the webpage

// import * as Departments from "./components/Departments";
import { Departments } from "./components/Departments";
import * as React from "react";

export class App extends React.Component {
  render() {
    return <div>
      <Departments />
    </div>
  }
}