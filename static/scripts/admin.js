$(document).ready(function(){
  $(".list_delete a").each(function(index){
    $(this).click(function(){
      return confirm("确定要删除该文章吗?") 
    });
  });
});
