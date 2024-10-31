const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const os = require('os');  // 운영체제 확인용
const app = express();

dotenv.config();

const PORT = process.env.PORT || 8002;
const API_URL = process.env.API_URL || 'http://localhost:3000';

// Python 경로 설정 (운영체제에 따라 다르게 설정)
const pythonPath = os.platform() === 'win32' 
    ? path.join(__dirname, 'venv', 'Scripts', 'python')
    : path.join(__dirname, 'venv', 'bin', 'python3');

app.use(
  cors({
    origin: API_URL,
    credentials: true,
  })
);

app.use(express.json());
app.use(bodyParser.json());

function runPythonScript(scriptName, args, res, inputData = null) {
  const scriptPath = path.join(__dirname, scriptName);

  // Python 프로세스를 실행할 때 PYTHONIOENCODING 환경 변수를 UTF-8로 설정
  const pythonProcess = spawn(pythonPath, [scriptPath, ...args], {
    env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
  });

  let responseData = '';

  if (inputData) {
    pythonProcess.stdin.write(JSON.stringify(inputData));
    pythonProcess.stdin.end();
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

// 유저 기반 추천 엔드포인트
app.post('/user-based/', (req, res) => {
  const inputRatingDict = req.body; // 클라이언트에서 받은 평점 데이터를 가져옴

  // Python 스크립트 호출 (명령어와 JSON 데이터를 전달)
  runPythonScript('recommender.py', ['user-based'], res, inputRatingDict);
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
