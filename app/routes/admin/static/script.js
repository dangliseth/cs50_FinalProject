$("form#addForm").on("submit", (event) => {
    console.log("Form submission intercepted!"); // Debug log
    event.preventDefault();

    const $form = $(event.target);
    const url = $form.attr("action");
    const formData = $form.serialize();

    $.post(url, formData).done((response) => {
        if (response.success) {
            window.location.href = response.redirect_url;
        }
    }).fail((xhr) => {
        console.log("AJAX request failed", xhr); // Debug log

        const message = xhr.responseJSON.error || "An error occurred while adding the subject.";

        const modal = $(".modal-body");
        
        modal.prepend(
            `<div id="error" class="alert alert-danger shadow" role="alert">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square-fill" viewBox="0 0 16 16">
                    <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm6 4c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995A.905.905 0 0 1 8 4m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                </svg>
                ${message}
            </div>`
        );

        setTimeout(() => {
            $("div#error").fadeOut("slow")
        }, 3000);
    });
});