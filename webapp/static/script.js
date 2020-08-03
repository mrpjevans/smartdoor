$(() => {
  $(".buttsonBar, .buttosnBar50").on("click", (e) => {
    const url = "/" + $(e.currentTarget).attr("data-event");

    $.getJSON(url, (data) => {
      if (data != true) {
        alert("Unexpected response from server!");
      } else {
        let tmpHtml = $(e.currentTarget).find(".buttonBarContainer").html();
        $(e.currentTarget)
          .find(".buttonBarContainer")
          .html('<i class="fas fa-check"></i>');
        setTimeout(() => {
          resetIcon(e.currentTarget, tmpHtml);
        }, 1000);
      }
    });
  });
});

function resetIcon(target, html) {
  $(target).find(".buttonBarContainer").html(html);
}

async function unlockDoor() {
  const button = $('[data-event=lock]').find('.buttonBarContainer')
  const oldHtml = button.html()
  button.html('<i class="fas fa-lock-open"></i>')
  await $.getJSON('/unlock')
  button.html(oldHtml)
}