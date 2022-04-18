import React from "react";
import "./Results.css";
import icon from "./kindle.png";
import axios from "axios";
import "react-awesome-button/dist/styles.css";
import logo from "./../search-component/main-logo.png";
import { useState } from "react";
import { useSelector } from "react-redux";

function Results(props) {
  const [input, setinput] = useState(props.phold);
  const token = useSelector((state) => state.jwtToken);
  const byCaller = (id, name, searchText) => {
    axios({
      method: "post",
      url: "http://127.0.0.1:5000/download/" + name,
      data: {},
      headers: {
        bookID: id,
        Token: token,
        search4: searchText,
      },
    }).then(console.log(id));
  };
  if (props.bookData.data != undefined) {
    // console.log(props.bookData);
    var listItems = props.bookData.data.map((elem, idx) => (
      <tr key={idx} scope="row">
        <td className="rowdet">{idx + 1}</td>
        <td className="rowdet">
          <a href="#">{elem.Author}</a>
        </td>
        <td className="rowdet">{elem.Title}</td>
        <td className="rowdet">{elem.Year}</td>
        <td className="rowdet">{elem.Size}</td>
        <td className="rowdet">
          <a href="#" title="">
            <img
              src={icon}
              className="resz zoom"
              onClick={() => {
                byCaller(elem.ID, elem.Title, elem.search4);
              }}
            />
          </a>
        </td>
      </tr>
    ));
  }

  return (
    <div>
      <img src={logo} alt="Logo" className="rect-logo" />
      <div className="container">
        <input
          className="form-control searcher"
          type="text"
          placeholder="Search book here .."
          value={input}
          onChange={(e) => {
            setinput(e.target.value);
          }}
        />
        <button
          type="primary"
          className="btn btn-primary rx-btn"
          onClick={() => {
            props.trig(input);
          }}
        >
          Search
        </button>
      </div>
      <div className="tabox">
        <div className="table-responsive custom-table-responsive">
          <table className="table custom-table">
            <thead>
              <tr>
                <th scope="col" className="rowdet">
                  Index
                </th>
                <th scope="col" className="rowdet">
                  Author
                </th>
                <th scope="col" className="rowdet">
                  Book Name
                </th>
                <th scope="col" className="rowdet">
                  Year
                </th>
                <th scope="col" className="rowdet">
                  Size
                </th>
                <th scope="col" className="rowdet">
                  Send to Kindle
                </th>
              </tr>
            </thead>
            <tbody>{listItems}</tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Results;
