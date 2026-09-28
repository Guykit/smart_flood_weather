async function province(){
    const provinceSelect=document.getElementById("provinceSelect");
    const re=await fetch("/api/provinces");
    const data=await re.json();

    data.forEach(function(row){
        const option=document.createElement("option");
        option.value=row.province_id;
        option.textContent=row.province_name;
        provinceSelect.appendChild(option);
    });
}

async function loadDate(){
    const dateSelect=document.getElementById("dateSelect");
    const re=await fetch("/api/dates");
    const data=await re.json();

    data.forEach(function(row){
        const option=document.createElement("option");
        option.value=row.date;
        option.textContent=row.date;
        dateSelect.appendChild(option);
    });
}

const provinceSelect=document.getElementById("provinceSelect");
const dateSelect=document.getElementById("dateSelect");

async function loadWeather(){
    const provinceid=provinceSelect.value;
    const date=dateSelect.value;

    if(!provinceid||!date){
        return;
    }

    const re=await fetch(
        "/api/weather/"+provinceid+"?date="+date
    );

    const data=await re.json();

    if(data.error){
        return;
    }

    document.getElementById("temperature").textContent=data.temperature;
    document.getElementById("humidity").textContent=data.humidity;
    document.getElementById("rainfall").textContent=data.rainfall;
    document.getElementById("rainfall_3d").textContent=data.rainfall_3d;
    document.getElementById("rainfall_7d").textContent=data.rainfall_7d;
    document.getElementById("windspeed").textContent=data.wind_speed;
    document.getElementById("riskDate").textContent="วันที่: "+data.date;

    if(data.flood_probability===null||data.flood_probability===undefined){
        document.getElementById("riskLevel").textContent="-";
        document.getElementById("floodPercent").textContent="-";
    }else{
        const percent=data.flood_probability*100;

        document.getElementById("floodPercent").textContent=
            percent.toFixed(2)+"%";

        if(percent>=70){
            document.getElementById("riskLevel").textContent="HIGH";
        }else if(percent>=40){
            document.getElementById("riskLevel").textContent="MEDIUM";
        }else{
            document.getElementById("riskLevel").textContent="LOW";
        }
    }
}

async function top4province(){
    const topprovince=document.getElementById("top4List");

    const re=await fetch("/api/top-province");
    const data=await re.json();

    topprovince.innerHTML="";

    data.forEach(function(row,index){
        const p=document.createElement("p");

        p.textContent=
            (index+1)+". "+
            row.province_name+" "+
            (row.flood_probability*100).toFixed(2)+"%";

        topprovince.appendChild(p);
    });
}

top4province();
province();
loadDate();

provinceSelect.addEventListener("change",function(){
    loadWeather();
});

dateSelect.addEventListener("change",function(){
    loadWeather();
});