import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import { useState } from 'react'
import { useForm } from "react-hook-form";
import { Container, Row, Col} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { CircularProgressbar,
  buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
 

function App() {


  const [seoData, setseoData] = useState(null)
  
  const { register, handleSubmit, formState: { errors } } = useForm();
 

  function getData() {
    axios({
      method: "GET",
      url:"http://localhost:5000/querry",
    })
    .then((response) => {
      const res =response.data
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}


   
    

  async function makeGetRequest(querry_data) {
      console.log(querry_data)
      let searchedQuerry = {
        "querry": querry_data
      };
      console.log(searchedQuerry)
      let res = await axios.post('http://localhost:5000/querry', searchedQuerry);
  
      let data = res.data;
 
      setseoData(({
        score: data.score,
        yourKeyword: data.yourKeyword,
        yourUrl: data.yourUrl,
        keywords: data.keywords,
        wordsAV: data.words,
        yourWords: data.yourWords,
        yourH1: data.yourH1,
        yourH1Correct: data.yourH1Correct,
        yourImg: data.yourIMG,
        minImg: data.imgMIN,
        maxImg: data.imgMAX

        
      }))

      
  }

 


  return (
    <div className="App">
      <header className="App-header"> 
        
       {!seoData && <div>
         
        <div className='Logo_main'>
            <h1>SeoOptymizer</h1>
            <h5 style={{ color: "#A209FF"}}>created by Mikołaj Kopciowski</h5> 
        </div>
        

        <form onSubmit={handleSubmit(makeGetRequest)}>
            <label className='inputLabel' htmlFor="url">Your website url:</label><br></br>
            <div>
                <input className="auditINPUT" placeholder="Input your url.." id="url" {...register('url', { required: true, maxLength: 150 })} />
                {errors.name && errors.name.type === "required" && <span>This is required</span>}
                {errors.name && errors.name.type === "maxLength" && <span>Max length exceeded</span> }
            </div>
            <label className='inputLabel'  htmlFor="name">Searched query:</label><br></br>
            <div>
                <input className="auditINPUT" placeholder="Input your query.."  id="keyword" {...register('keyword', { required: true, maxLength: 50 })} />
                {errors.name && errors.name.type === "required" && <span>This is required</span>}
                {errors.name && errors.name.type === "maxLength" && <span>Max length exceeded</span> }
            </div>


            <input className="sendDataBtn" type="submit"   value="Send"/>
        </form>
         
          </div>
         }

    
        
          
        {seoData && <div className='audit'>

        <Container>
            <Row>
              <Col sm={2} >
                <div className="stickyLeft">

                <div className='Logo'>
                  <img src={require('./img/logo.png') } class="logo"/>
                </div>
                <div className='linki'>
                  <p><a href='#topKW'  className='link'><strong className='linkFirstLetter'>K</strong>eyword</a></p>
                  <p><a href='#score'  className='link'><strong className='linkFirstLetter'>S</strong>core</a></p>
                  <p><a href='#keyWords'  className='link'><strong className='linkFirstLetter'>K</strong>eywords</a></p>
                  <p><a href='#words'  className='link'><strong className='linkFirstLetter'>W</strong>ords</a></p>
                  <p><a href='#structure'  className='link'><strong className='linkFirstLetter'>S</strong>tructure</a></p>
                  <p><a href='#images'  className='link'><strong className='linkFirstLetter'>I</strong>mages</a></p>

                </div>
                </div>


              </Col>

            <Col >

            <p id="topKW" className='yourKWstyle'>Your <strong className='yourKWpurple'>Query</strong></p>
            <h1 className='keywordStyle'>{seoData.yourKeyword}</h1>
            <p className='yourUrlStyle'>url: {seoData.yourUrl}</p>


            <h2 className='sectionName' id='score'>Score <strong className='linkFirstLetter'>_______</strong></h2>                
            
            <Row>
              <Col sm={2} style={{ margin: "auto" }}>
              <h3>Your Score: <strong className='linkFirstLetter'>{seoData.score}</strong>/100 </h3>
           
              </Col>
              <Col>
              <div style={{ width: 70, height: 70 }}>
               
             
              
             
            
               
              <CircularProgressbar
                
                
                value={seoData.score}
                strokeWidth={50}
                styles={buildStyles({
                  strokeLinecap: "butt",
                  pathColor: "#A209FF",
                })}
              />

            

            </div>
              </Col>
            </Row>
            
               
            
            

            <h2 className='sectionName' id='keyWords'>Keywords <strong className='linkFirstLetter'>_______</strong></h2>                

            <table>
              

              <h4 className='keywordX'><strong>Single Keywrods</strong></h4>
              <tr className='tableTop'>
                <th>Keyword</th>
                <th>Average</th> 
                <th>Your</th> 
                <th>Difference</th> 
              </tr>  
              {seoData.keywords.x1.map(item => (
                
                <tr className='blackbar'>
                  <th key={item}>{item[0]}</th>
                  <th key={item}>{item[1]}</th>
                  <th key={item}>{item[2]}</th>

                  <th key={item}>
                  {item[3] >= 10 && <div className='redKeyword'>
                      {item[3]}
                    </div>    
                  } 
                  {10 > item[3] && item[3] >= 3 && <div className='orangeKeyword'>
                      {item[3]}
                    </div>    
                  } 
                  { item[3] < 3 && <div className='greenKeyword'>
                      {item[3]}
                    </div>    
                  } 



                  
                  </th>
                </tr>  
                ))}

                <h4 className='keywordX'><strong>Double Keywrods</strong></h4>
                <tr className='tableTop'>
                <th>Keyword</th>
                <th>Average</th> 
                <th>Your</th> 
                <th>Difference</th> 
                </tr>  
                {seoData.keywords.x2.map(item => (
                
                <tr className='blackbar'>
                  <th key={item}>{item[0]}</th>
                  <th key={item}>{item[1]}</th>
                  <th key={item}>{item[2]}</th>
                  <th key={item}>
                  {item[3] >= 10 && <div className='redKeyword'>
                      {item[3]}
                    </div>    
                  } 
                  {10 > item[3] && item[3] >= 3 && <div className='orangeKeyword'>
                      {item[3]}
                    </div>    
                  } 
                  { item[3] < 3 && <div className='greenKeyword'>
                      {item[3]}
                    </div>    
                  } 
                  </th>
                </tr>  
                ))}



            </table>


            <h2 className='sectionName' id='words'>Words <strong className='linkFirstLetter'>_______</strong></h2>     
            <h5><strong>Difference: {(seoData.yourWords - seoData.wordsAV).toFixed(1)}</strong></h5>      
            <h6>The number of words on your website: {seoData.yourWords}</h6>
            <h6>Average number of words on websites: {seoData.wordsAV}</h6> 


            <h2 className='sectionName' id='structure'>Header 1 <strong className='linkFirstLetter'>_______</strong></h2>                
            <h6>Your H1: {seoData.yourH1}</h6>


            {seoData.yourH1Correct == "True" && <div>

            <p>Your header is correct</p> 

            </div>
            }

            {seoData.yourH1Correct === "False" && <div>
            <p>Your header is incorrect</p> 
            <h5 className='poprawNaglowek'>Correct the header!</h5> 

            </div>
            }


            <h2 className='sectionName' id='images'>Images <strong className='linkFirstLetter'>_______</strong></h2>                
            <p>Number of photos on your website: <strong>{seoData.yourImg}</strong></p>
            <p>Preferred number of photos on your website: <strong>{seoData.minImg} - {seoData.maxImg}</strong></p>



              </Col>
              </Row>
              
            </Container>
            </div>
      
            } 

            

        
       


      </header>
    </div>
  );
}

export default App;
