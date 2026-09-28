
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f7f9;
    color: #333;
}

.container {
    width: 90%;
    max-width: 1000px;
    margin: 40px auto;
}

h1 {
    text-align: center;
    margin-bottom: 8px;
    color: #1f4e5f;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 30px;
}

.card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card h2 {
    margin-top: 0;
    color: #2f6475;
}

select {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 6px;
    background: white;
}

.risk-card {
    text-align: center;
}

.risk-level {
    font-size: 32px;
    font-weight: bold;
    margin: 15px 0;
}

.percentage {
    font-size: 26px;
    font-weight: bold;
    color: #2f6475;
    margin: 10px 0;
}

#riskDate {
    color: #777;
}

.weather {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.weather .card {
    text-align: center;
    margin-bottom: 0;
}

.weather .card h2 {
    font-size: 18px;
}

.value {
    font-size: 28px;
    font-weight: bold;
    color: #333;
}

@media (max-width: 700px) {

    .weather {
        grid-template-columns: 1fr;
    }

    .container {
        width: 95%;
        margin: 20px auto;
    }
}

