import React from "react";
import "./Results.css";
import icon from "./kindle.png";
import axios from "axios";

function Results(props) {
  const byCaller = (link, name) => {
    const headers = {
      dlink: link,
    };
    // axios
    //   .post("https://127.0.0.1:5000/download/" + name, { headers: headers })
    //   .then(console.log("done!!!!"));
    axios({
      method: "post", //you can set what request you want to be
      url: "http://127.0.0.1:5000/download/" + name,
      data: {},
      headers: {
        dlink: link,
      },
    }).then(console.log(link));
  };

  if (props.bookData.data != undefined) {
    console.log(props.bookData);
    var listItems = props.bookData.data.map((elem) => (
      <tr key={elem.index} scope="row">
        <td className="rowdet">{elem.index}</td>
        <td className="rowdet">
          <a href="#">{elem.Author}</a>
        </td>
        <td className="rowdet">{elem.Title}</td>
        <td className="rowdet">{elem.size}</td>
        <td className="rowdet">
          <img
            src={icon}
            className="resz"
            onClick={() => {
              byCaller(elem.download_link, elem.Title);
            }}
          />
        </td>
      </tr>
    ));
  } else {
    return <div></div>;
  }

  return (
    <div>
      <div>
        <div className="table-responsive custom-table-responsive">
          <table className="table custom-table">
            <thead>
              <tr>
                <th scope="col">Index</th>
                <th scope="col">Author</th>
                <th scope="col">Book Name</th>
                <th scope="col">Size</th>
                <th scope="col">#</th>
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
