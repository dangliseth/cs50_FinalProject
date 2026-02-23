$("form#add-subjectForm").on("submit", (event) => {
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

        const modal = $("#add-subjectBody");
        
        modal.prepend(
            `<div id="error" class="alert alert-danger shadow" role="alert">
                <i class="fa-solid fa-triangle-exclamation"></i>
                ${message}
            </div>`
        );

        setTimeout(() => {
            $("div#error").fadeOut("slow")
        }, 3000);
    });
});

$("button#add-subject-btn").on("click", () => {
    const container = $("#subject-container");
    // Find the first subject entry to use as a template
    const original = container.find(".subject-entry:first");
    const clone = original.clone();

    // Find the select and label within the cloned element
    const select = clone.find("select");
    const labelSubject = clone.find("label[for^='subject-code']");
    const labelRequired = clone.find("label[for^='required']");
    const checkbox = clone.find("input[type='checkbox']");

    // Create a new unique ID. Counting existing subject entries is more robust
    // than counting all children, in case other elements are present.
    const newIdSubject = "subject-code-" + container.children(".subject-entry").length;
    const newIdRequired = "required-" + container.children(".subject-entry").length;

    // Set the new ID on the select, reset its value, and link the label to it
    select.attr("id", newIdSubject).prop("selectedIndex", 0);
    select.attr("name", newIdSubject);
    checkbox.attr("name", newIdRequired);
    checkbox.attr("id", newIdRequired);
    checkbox.prop("checked", false);
    labelSubject.attr("for", newIdSubject);
    labelRequired.attr("for", newIdRequired);


    // Add the newly created element to the DOM
    container.append(clone);
});

$("form#add-student").on("click", "button#add-enrollment-btn", function() {
    const container = $("#enrollment-container");
    const btn = $(this);



    const newElement = `<div class="col-md d-flex">
                        <select class="form-select">
                            <option value="" selected>Select a Program</option>
                            {% for prog in programNames %}
                                <option value="{{ prog }}">{{ prog }}</option>
                            {% endfor %}
                        </select>
                        <button type="button" class="btn btn-sm ms-2" id="delete-enroll-program">
                            <i class="fa-solid fa-minus"></i>
                        </button>
                    </div>`;
    container.prepend(newElement);


    if (container.children().length >= 2) {
        btn.remove();
    } else {
        container.before(btn);
    };
});

$("form#add-programForm").on("submit", (event) => {
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
        const errorType = xhr.responseJSON.errorType || "error";

        const modal = $("#add-programBody");
        
        modal.prepend(
            `<div id="error" class="alert alert-${errorType} shadow" role="alert">
                <i class="fa-solid fa-triangle-exclamation"></i>
                ${message}
            </div>`
        );

        setTimeout(() => {
            $("div#error").fadeOut("slow")
        }, 3000);
    });
});

