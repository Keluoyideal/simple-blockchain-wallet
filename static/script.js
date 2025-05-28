function mineBlock() {
  $.get("/mine_block", function(data) {
    alert("挖礦成功！新增區塊：" + data.block.index);
    loadChain();
  });
}

function addTransaction() {
  const sender = $("#sender").val();
  const recipient = $("#recipient").val();
  const amount = parseFloat($("#amount").val());

  $.ajax({
    url: "/add_transaction",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      sender: sender,
      recipient: recipient,
      amount: amount
    }),
    success: function(data) {
      alert(data.message);
    }
  });
}

function loadChain() {
  $.get("/get_chain", function(data) {
    $("#chain-output").text(JSON.stringify(data.chain, null, 2));
  });
}

$(document).ready(loadChain);


function mineBlock() {
    axios.get('/mine_block').then(res => {
        alert('✅ 區塊已挖出並加入鏈中！\n\n區塊編號：' + res.data.block.index);
        getChain(); // 更新區塊鏈顯示
    }).catch(err => {
        alert('❌ 挖礦失敗：' + (err.response?.data || err.message));
    });
}
