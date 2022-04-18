import { createStore } from "redux";

const obj = {
  jwtToken: "",
  haveToken: false,
};
const reducerfn = (state = obj, action) => {
  if (action.type === "UPDATE_TOKEN") {
    return {
      ...state,
      haveToken: !state.haveToken,
      jwtToken: action.jwtToken,
    };
  }
  if (action.type === "FORGET_TOKEN") {
    return {
      ...state,
      haveToken: !state.haveToken,
      jwtToken: "",
    };
  }
  return state;
};
const store = createStore(reducerfn);

export default store;
