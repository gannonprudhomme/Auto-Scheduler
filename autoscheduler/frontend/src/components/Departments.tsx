// This is just a sample of a page, it won't actually be used
import * as React from "react";

// I have no idea why this won't work
// import TextField from "@material-ui/core/TextField";

export class Departments extends React.Component {
  handleSubmit(e: any) {
    var val = e;
    console.log(e)
  }

  handleChange(x: any) {
    console.log(x)
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        {/* <TextField
          id='someId'
          label="Department Search"
          value="Enter Department"
          onChange={this.handleChange}
          variant="outlined"
        /> */}
      </form>
    );
  }
}