import logo from './logo.svg';
import './App.css';
//import './Korean.css';
//import './Japen.css';
import { useState } from 'react';

function App() {

  let post= '소리가 들리시면 손을 움직여 주세요'
  let [음식, b] = useState(['한식','일식' ,'중식']);
  let [선택, 주문] = useState(0);

  return (
    <div className="App">
      <div className="black-nav">
        <h4 style={{cloe : 'skyblue', fontsize : '50px'}}> 안내를 시작합니다</h4>
      </div>
      <h4>{ post }</h4>
      <h4>...잠시만 기다려 주십시오</h4>
      <h4>인식이 완료 되었습니다</h4>
      <div className='list'>
        <h4>한식</h4>
        <p>{ 음식[0] } <span onClick={()=>{선택(주문+1)}}>돌솥비빔밥 ✔</span>{주문}</p>
        <p>- 찌개</p>
        <p>- 떡갈비</p>
        </div>
      <div className='list'>
        <h4>일식</h4>
        <p>- 돈카츠</p>
        <p>- 초밥</p>
        <p>- 라멘</p>
        </div>
      <div className='list'>
        <h4>중식</h4>
        <p>- 마라탕</p>
        <p>- 유산슬</p>
        <p>- 탕수육</p>
        </div>   
    </div>
  );
}

export default App;
