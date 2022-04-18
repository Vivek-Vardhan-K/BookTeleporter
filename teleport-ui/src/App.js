import axios from "axios";
import { useEffect } from "react";
import "./App.css";
import Search from "./search-component/Search";
import { useDispatch } from "react-redux";

function App() {
  const dispatch = useDispatch();
  const loadDataOnlyOnce = () => {
    axios.get("http://127.0.0.1:5000/getToken").then((res) => {
      console.log(res.data);
      dispatch({
        type: "UPDATE_TOKEN",
        jwtToken: res.data,
      });
    });
  };

  useEffect(() => {
    loadDataOnlyOnce();
  }, []);
  return (
    <div className="App">
      <Search />
    </div>
  );
}

export default App;
