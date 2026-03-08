// remove flash messages after 3 seconds.
setTimeout(() => {
    $("div.flashes").fadeOut("slow")
}, 3000)

$("button, a").hover(
    function() {$(this).find("i[class*='fa-']").addClass("fa-beat");}, 
    function() {$(this).find("i[class*='fa-']").removeClass("fa-beat");}
);

$("a#logout-btn").hover(function() {
    const $icon = $(this).find("i");

    $icon.stop(true, true).fadeOut(150, function() {
        $(this).removeClass("fa-building-circle-arrow-right")
                .addClass("fa-person-running")
                .fadeIn(150);
    });
}, function() {
    const $icon = $(this).find("i");

    $icon.stop(true, true).fadeOut(150, function() {
        $(this).removeClass("fa-person-running")
                .addClass("fa-building-circle-arrow-right")
                .fadeIn(150);
    });
});

$("nav div[class$='-dropdown']").hover(function() {
    $(this).addClass("position-relative");
    const items = $(this).find("div[class^='dropdown']");

    items.removeClass("d-none").addClass("d-grid");
}, function() {
    const items = $(this).find("div[class^='dropdown']");

    items.addClass("d-none").removeClass("d-grid");
});

// handle login modal.
$("#loginForm").on("submit", (event) => {
    // stop form action from running.
    event.preventDefault();

    // get form data.
    const $form = $(event.target); // $(this) can be used if the standard function() is used.
    const url = $form.attr("action");
    const formData = $form.serialize();

    // setup AJAX post.
    $.post(url, formData).done((response) => {
        // login success.
        if (response.success) {
            window.location.href = response.redirect_url;
        }
    })
    .fail(() => {
        // login fail.
        const modalBody = $(".modal-body");

        // create and display the login error alert.
        modalBody.prepend(
            `<div id="error" class="alert alert-danger shadow" role="alert">
                <i class="fa-solid fa-circle-exclamation"></i> Invalid credentials.
            </div>`
        );

        // remove login error alert after 3 seconds.
        setTimeout(() => {
            $("div#error").fadeOut("slow")
        }, 3000);
    })
});

$("#loginModal").on("shown.bs.modal", function() {
    $("#username").focus();
});

// Use event delegation on the container to handle events for all select elements,
// including ones that are added dynamically.
$(document).on("change", "select", (event) => {
    // Find the placeholder option within the specific select that was changed and disable it.
    $(event.target).find('option[value=""]').prop("disabled", true);
});