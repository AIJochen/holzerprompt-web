(function () {
    "use strict";

    function updateBlockFields(select) {
        const blockType = select.value;

        /*
         * Bei Inline-Blöcken begrenzen wir die Suche auf den jeweiligen
         * Inline-Datensatz. Beim normalen PageBlockAdmin verwenden wir
         * das gesamte Dokument.
         */
        const scope =
            select.closest(".inline-related") ||
            document;

        const heroFields =
            scope.querySelectorAll(".hero-fields");

        const richTextFields =
            scope.querySelectorAll(".rich-text-fields");

        heroFields.forEach(function (field) {
            field.style.display =
                blockType === "hero" ? "" : "none";
        });

        richTextFields.forEach(function (field) {
            field.style.display =
                blockType === "rich_text" ? "" : "none";
        });
    }

    function initializeBlockTypeSelects(root) {
        const container = root || document;

        const selects =
            container.querySelectorAll(
                'select[name$="block_type"]'
            );

        selects.forEach(function (select) {
            updateBlockFields(select);

            if (!select.dataset.blockTypeListener) {
                select.addEventListener(
                    "change",
                    function () {
                        updateBlockFields(select);
                    }
                );

                select.dataset.blockTypeListener = "true";
            }
        });
    }

    document.addEventListener(
        "DOMContentLoaded",
        function () {
            initializeBlockTypeSelects(document);
        }
    );

    /*
     * Django feuert dieses Ereignis, wenn dynamisch ein neuer
     * Inline-Datensatz hinzugefügt wird.
     */
    document.addEventListener(
        "formset:added",
        function (event) {
            initializeBlockTypeSelects(
                event.target
            );
        }
    );
})();