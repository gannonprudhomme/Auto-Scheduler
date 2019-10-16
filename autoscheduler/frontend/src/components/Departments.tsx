// This is just a sample of a page, it won't actually be used
import * as React from "react";

// I have no idea why this won't work
// import TextField from "@material-ui/core/TextField";

// Not how you should use props, but should be fine
interface DepartmentsProps {
  value: any
  depts: Array<string>
}

interface DepartmentsState { 
  value: string
  depts: Array<any>
}

export class Departments extends React.Component<DepartmentsProps, any> {
  constructor(props: DepartmentsProps) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.state = { value: "" }
  }

  handleSubmit(e: any) {
    console.log(this.state.value)
    fetch(`/api/depts/${this.state.value}`).then((response) => {
    })
  }

  handleChange(e: any) {
    this.setState({ value : e.target.value })
    fetch(`/api/depts/${this.state.value}`)
    .then((resp) => resp.json())
    .then((response) => {
      this.setState({depts: response})
      console.log(response)
      // Convert response to depts object
      // Which will then be used to render 
    }).catch((error) => {

    });
  }

  render() {
    return (
      <div>
        <form id="input" onSubmit={this.handleSubmit} onChange={this.handleChange}>
          <label>
            Dept:
            <input type="text"/>
          </label>
        </form>
        <div id="output">
          {/* {this.state.depts} */}
        </div>
      </div>
    );
  }
}