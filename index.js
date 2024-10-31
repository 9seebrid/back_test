const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const app = express();

dotenv.config();

const PORT = process.env.PORT || 8002; // 환경변수 PORT 사용
const API_URL ='http://localhost:3000/' // API_URL 환경변수 사용

app.use(
  cors({
    origin: API_URL, // 환경 변수로부터 API URL을 가져옴
    credentials: true,
  })
);

app.use(express.json());
app.use(bodyParser.json());

// 공통 파이썬 스크립트 실행 함수
function runPythonScript(scriptName, args, res, inputData = null) {
  const scriptPath = path.join(__dirname, scriptName);
  const pythonPath = path.join(__dirname, 'venv', 'bin', 'python3'); // 로컬 경로
  const pythonProcess = spawn(pythonPath, [scriptPath, ...args]);

  let responseData = '';

  // Python 스크립트로 데이터를 전달 (JSON 형식으로 전달)
  if (inputData) {
    pythonProcess.stdin.write(JSON.stringify(inputData)); // 입력 데이터를 stdin으로 전달
    pythonProcess.stdin.end(); // 데이터 전송 완료 후 stdin 종료
  }

  pythonProcess.stdout.on('data', (data) => {
    responseData += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code === 0) {
      try {
        const jsonResult = JSON.parse(responseData);
        res.status(200).json(jsonResult);
      } catch (error) {
        console.error('Invalid JSON response from Python script:', error);
        res.status(500).json({ error: 'Invalid JSON response from Python script' });
      }
    } else {
      console.error(`Child process exited with code ${code}`);
      res.status(500).json({ error: `Python process exited with code ${code}` });
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
}

app.get('/', (req, res) => {
  res.send('Hello World! movie-back');
});

// 랜덤 영화 엔드포인트
app.get('/random/:count', (req, res) => {
  const { count } = req.params;
  runPythonScript('movie_random.py', [count], res);
});

// 최신 영화 엔드포인트
app.get('/latest/:count', (req, res) => {
  const { count } = req.params;
  runPythonScript('movie_latest.py', [count], res);
});

// 장르별 영화 엔드포인트
app.get('/genres/:genre/:count', (req, res) => {
  const { genre, count } = req.params;
  runPythonScript('movie_genres.py', [genre, count], res);
});

// 아이템 기반 추천 엔드포인트
app.get('/item-based/:item', (req, res) => {
  const { item } = req.params; // item 파라미터를 가져옴
  console.log(`Item-based recommendation for item: ${item}`); // 콘솔에 item 값을 찍음
  runPythonScript('recommender.py', ['item-based', item], res); // Python 스크립트 호출 (명령어와 item ID 전달)
});

// 유저 기반 추천 엔드포인트
app.post('/user-based/', (req, res) => {
  const inputRatingDict = req.body; // 클라이언트에서 받은 평점 데이터를 가져옴

  // Python 스크립트 호출 (명령어와 JSON 데이터를 전달)
  runPythonScript('recommender.py', ['user-based'], res, inputRatingDict);
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
