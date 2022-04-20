import React from "react";
import { useState } from "react";
import "./search-component.css";
import logo from "./main-logo.png";
import axios from "axios";
import Results from "../results-component/Results";
import { useSelector } from "react-redux";

function Search() {
  const [input, setInput] = useState("");
  const [search, setSearch] = useState(false);
  const [bookData, setBookData] = useState([]);
  const token = useSelector((state) => state.jwtToken);
  const searchHandler = (inp) => {
    console.log(inp);
    console.log("ran bois");
    axios({
      method: "get",
      url: `https://teleportx.herokuapp.com//search/` + inp,
      data: {},
      headers: {
        Token: token,
      },
    }).then((res) => {
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
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            type="button"
            className="btn btn-outline-primary"
            onClick={() => {
              searchHandler(input);
            }}
          >
            search
          </button>
        </div>
      </div>
    );
  else {
    return <Results bookData={bookData} phold={input} trig={searchHandler} />;
  }
}

export default Search;
