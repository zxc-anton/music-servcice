import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Кастомная метрика для отслеживания процента ошибок
const errorRate = new Rate('errors');

export const options = {
  stages: [
    // Плавно увеличиваем нагрузку от 1 до 100 VU за 2 минуты
    { duration: '2m', target: 100 },
    // Держим 100 VU еще 2 минуты
    { duration: '2m', target: 100 },
    // Плавно увеличиваем до 200 VU
    { duration: '2m', target: 200 },
    { duration: '2m', target: 200 },
    // И так далее...
    { duration: '2m', target: 300 },
    { duration: '2m', target: 300 },

  ],
  thresholds: {
    errors: ['rate<0.05'], // Не более 5% ошибок
    http_req_duration: ['p(95)<500'], // 95% запросов быстрее 500ms
  },
};

export default function () {
  const res = http.get('http://127.0.0.1:8000/api/stream/3');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  
  // Отмечаем ошибку если статус не 2xx/3xx
  errorRate.add(res.status >= 400);
  
  sleep(1);
}