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

    const subjEntryCount = container.children(".subject-entry").length;
    if (subjEntryCount > 0) {
        clone.append(`<button type="button"  class="btn btn-outline-danger btn-sm remove-subject-btn">
                        Remove <i class="fa-solid fa-square-minus"></i>
                    </button>`)
    };

    // Add the newly created element to the DOM
    container.append(clone);
});

// Example of how to handle the click for this new button
$("#subject-container").on("click", ".remove-subject-btn", function() {
    $(this).closest(".subject-entry").remove();
});


$("form#add-student").on("click", "button#add-enrollment-btn", function() {
    const container = $("#enrollment-container");
    const btn = $(this);

    const programsData = container.attr("data-programs");
    const programs = JSON.parse(programsData);
    const optionsHTML = programs.map(prog =>
        `<option value="${prog}">${prog}</option>`
    ).join("");


    const newElement = `<div class="col-md d-flex">
                        <select class="form-select" name="programNames">
                            <option value="" selected>Select a Program</option>
                            ${optionsHTML}
                        </select>
                        <button type="button" class="btn btn-sm ms-2" id="delete-enroll-program">
                            <i class="fa-solid fa-minus"></i>
                        </button>
                    </div>`;
    container.append(newElement);


    if (container.children().length >= 2) {
        btn.remove();
    };
});

$("form#add-student").on("click", "button#delete-enroll-program", function() {
    const btn = $(this);
    const parent = btn.parent();
    parent.remove();

    const container = $("#enrollment-container");
    if (container.children().length < 2 && !$("#add-enrollment-btn").length) {
        const addBtn = `<button type="button" id="add-enrollment-btn" class="btn btn-outline-secondary">
                        Add A Program<i class="fa-solid fa-plus fa-fade"></i>
                        </button>`;
        container.before(addBtn);
    };
});

$("form#edit-studentForm").on("click", "button#edit-btn", function() {
    const button = $(this);
    const input = button.parent().find("input");

    if (input.prop("disabled")){
        input.prop("disabled", false);
        const icon = button.find("i");
        icon.removeClass("fa-regular fa-pen-to-square").addClass("fa-solid fa-arrow-rotate-left");
        button.removeClass("btn-outline-primary").addClass("btn-warning");
        button.empty().append(icon).append("Undo");
    } else {
        input.prop("disabled", true);
        const icon = button.find("i");
        icon.removeClass("fa-solid fa-arrow-rotate-left").addClass("fa-regular fa-pen-to-square");
        button.removeClass("btn-warning").addClass("btn-outline-primary");
        button.empty().append(icon).append("Edit");
        input.val(input.attr("value")); // Reset to original value
    };
});


$("form").on("submit", function(event) {
    event.preventDefault();

    const $form = $(this);
    const url = $form.attr("action");
    const formData = $form.serialize();

    $.post(url, formData).done((response) => {
        if (response.success) {
            window.location.href = response.redirect_url;
        }
    }).fail((xhr) => {
        const message = xhr.responseJSON.error || "Database Error.";
        const errorType = xhr.responseJSON.errorType || "danger";

        const modal = $(".modal-body");
        
        modal.prepend(
            `<div id="error" class="alert alert-${errorType} shadow mt-5" role="alert">
                <i class="fa-solid fa-triangle-exclamation"></i>
                ${message}
            </div>`
        );

        setTimeout(() => {
            $("div#error").fadeOut("slow")
        }, 3000);
    });
});

$("#btn-confirm-drop").on("click", function() {
    const form = $("form#drop-subjectsForm");
    const checked = form.find("input[name='programs']:checked");

    if (checked.length === 0) {
        Swal.fire({
            icon: "warning",
            title: "No Selection",
            text: "Please select at least one program to drop."
        });
    } else {
        let listHtml = '<ul class="list-group list-group-flush text-start">';
        checked.each(function() {
            const labelText = form.find(`label[for='${this.id}']`).text();
            listHtml += `<li class="list-group-item px-0">${labelText}</li>`;
        });
        listHtml += '</ul>';
        
        Swal.fire({
            title: "Are you sure?",
            html: `<p>You are about to drop the following programs:</p>${listHtml}`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#dc3545",
            cancelButtonColor: "#6c757d",
            confirmButtonText: "Yes, drop them!"
        }).then((result) => {
            if (result.isConfirmed) {
                form.submit();
            }
        });
    }
});