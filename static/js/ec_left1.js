var ec_left1=echarts.init(document.getElementById("l1"),"dark");
ec_left1_option = {
  title: {
      text: '全国累计趋势',
      textStyle:{

      },
      left:"left"
  },
  tooltip: {
      trigger: 'axis',
      axisPointer:{
        type:"line",
        lineStyle:{
          color:"#7171C6"
        }
      }
  },
  legend: {
      data: ['累计确证', '现有疑似', '累计治愈', '累计死亡'],
      left:"right"
  },
  grid: {
      left: '4%',
      right: '6%',
      bottom: '4%',
      top:50,
      containLabel: true
  },
  xAxis: [{
      type: 'category',
      boundaryGap: false,
      data: []
  }],
  yAxis:[{
      type: 'value',
      axisLable:{
        show:true,
        color:"white",
        fontSize:12,
        formatter:function(value){
          if(value>=1000){
            value=value/1000+"k";
          }
          return value;
        }
      },
      axisLine:{
        show:true
      },
      splitLine:{
        show:true,
        lineStyle:{
          color:"#17273B",
          width:1,
          type:"solid"
        }
      }
  }],
  series: [
      {
          name: '累计确诊',
          type: 'line',
          smooth:true,
          data: []
      },
      {
          name: '现有疑似',
          type: 'line',
          smooth:true,
          data: []
      },
      {
          name: '累计治愈',
          type: 'line',
          smooth:true,
          data: []
      },
      {
          name: '累计死亡',
          type: 'line',
          smooth:true,
          data: []
      }
  ]
};
