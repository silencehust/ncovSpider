var ec_right2=echarts.init(document.getElementById("r2"),"dark");
var worddate=[]
ec_right2_option = {
  title: {
      text: '今日疫情热搜',
      textStyle:{
          color:"white"
      },
      left:"left"
  },
  tooltip: {
      show:false
  },
  series: [
      {
        type: 'wordCloud',
        gridSize:1,sizeRange:[12,55],
        rotationRange:[-45,0,45,90],
        textStyle:{
            normal:{
              color:function(){
                return "rgb("+Math.round(Math.random()*255)+","+Math.round(Math.random()*255)+","+Math.round(Math.random()*255)+")"
              }
            }
        },
        right:null,
        bottom:null,
        data:worddate
      }
  ]
};
