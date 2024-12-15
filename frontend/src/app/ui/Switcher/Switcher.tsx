'use client'
import { useState } from "react";
import styles from "./style.module.scss";
import { SwitcherType } from "./types";
import entStyles from "../../entities.module.scss";

const getGradientValue = (values: string[], current: string) => {
  let gradientString;
  const selectedIndex = values.findIndex(el => el === current);
  if (selectedIndex === 0) {
    gradientString = "linear-gradient(to right, #000, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.7), rgba(255, 255, 255, 0.3) )";
  } else if (selectedIndex === values.length - 1) {
    gradientString = "linear-gradient(to right, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9), #000)";
  } else {
    gradientString = "linear-gradient(to right, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.8), #000, rgba(0, 0, 0, 0.8), rgba(255, 255, 255, 0.3))";
  }

  return gradientString;
}


export const Switcher = function({
  values,
  setNewValue,
  initValue=values[0],
} : SwitcherType) {
  const [ selectedItem, onChangeItem ] = useState(initValue);
  
  const gradientValue = getGradientValue(values, selectedItem);
  const selectedIndex = values.findIndex(el => el === selectedItem);
  const gradientStyle = {
    "backgroundImage": gradientValue,
    "width": `${100 / values.length}%`,
    "marginLeft": `${100 * selectedIndex / values.length}%`,
    "transition": "all 0.1s linear",
    "height": "100%",
    "zIndex": "2",
  }
  return (
    <div className={styles.switcher_wrapper}>
      <div className={entStyles.flex_around}>
        {values.map((value, idx) => {

          const className = value === selectedItem 
            ? `${styles.value_span} ${styles.value_span_selected}` 
            : `${styles.value_span}`;

          return (
            <span
              key={idx}
              className={className}
              onClick={(e: React.MouseEvent<HTMLSpanElement>) => {
                if (e.currentTarget.innerHTML === selectedItem) return;
                setNewValue(e.currentTarget.innerHTML);
                onChangeItem(e.currentTarget.innerHTML);
              }}
    
            >{value}</span>
          )
        })}
      </div>
      <div 
      style = {{
        height: "3px",
        backgroundColor: "white",
      }}
      className={`${styles.gradient_line_simple}`}>
        <div
          style={gradientStyle}
          className={styles.gradient_small_line}
        />
      </div>
    </div>
  )
}
