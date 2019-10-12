// This is just a sample of a page, it won't actually be used
import * as React from "react";

// I have no idea why this won't work
// import TextField from "@material-ui/core/TextField";

interface DepartmentsProps {
  value: any
}

export class Departments extends React.Component<DepartmentsProps> {
  constructor(props: DepartmentsProps) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(e: any) {
    console.log(this.props.value)
    fetch(`/api/depts?v=${this.props.value}`).then((response) => {
      console.log(response)
    })
  }

  handleChange(e: any) {

  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} onChange={this.handleChange}>
        <label>
          Dept:
          <input type="text"/>
        </label>
      </form>
    );
  }
}