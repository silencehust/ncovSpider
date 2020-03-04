var ec_right1=echarts.init(document.getElementById("r1"),"dark");
ec_right1_option = {
  title: {
      text: '非湖北地区城市确诊TOP5',
      textStyle:{
          color:"white"
      },
      left:"left"
  },
  color:["#3398D8"],
  tooltip: {
      trigger: 'axis',
      axisPointer:{
        type:"shadow",
      }
  },
  xAxis:[{
      type: 'category',
      data: []
  }],
  yAxis:[{
      type: 'value'
  }],
  series: [
      {
        data: [],
        type: 'bar',
        barMaxWidth:"50%"
      }
  ]
};
