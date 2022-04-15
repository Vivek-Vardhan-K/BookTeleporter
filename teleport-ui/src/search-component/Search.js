import React from "react";
import { useState } from "react";
import "./search-component.css";
import logo from "./main-logo.png";
import axios from "axios";
import Results from "../results-component/Results";

function Search() {
  const [input, setInput] = useState("");
  const [search, setSearch] = useState(false);
  const [bookData, setBookData] = useState([]);
  var searchHandler = (e) => {
    axios.get(`http://127.0.0.1:5000/search/` + input).then((res) => {
      // console.log(res.data);
      setSearch(true);
      setBookData(res.data);
    });
  };
  if (!search)
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
  else {
    return <Results bookData={bookData} />;
  }
}

export default Search;
