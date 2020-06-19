Handlebars.registerHelper('inc', function (number, options) {
    if (typeof (number) === 'undefined' || number === null)
        return null;

    // Increment by inc parameter if it exists or just by one
    return number + (options.hash.inc || 1);
});