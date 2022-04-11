import React from "react";
import { useState } from "react";
import "./search-component.css";
import logo from "./main-logo.png";
import axios from "axios";

function Search() {
  const [input, setInput] = useState("");
  var searchHandler = (e) => {
    console.log(input);
    axios
      .get(`http://127.0.0.1:5000/search/` + input)
      .then(console.log("done"));
  };
  return (
    <div>
      <img src={logo} alt="Logo" className="logo-pos" />
      <div className="input-group vertical-center inner">
        <input
          type="search"
          value={input}
          className="form-control rounded"
          placeholder="Search"
          aria-label="Search"
          aria-describedby="search-addon"
          onInput={(e) => setInput(e.target.value)}
        />
        <button
          type="button"
          className="btn btn-outline-primary"
          onClick={searchHandler}
        >
          search
        </button>
      </div>
    </div>
  );
}

export default Search;
