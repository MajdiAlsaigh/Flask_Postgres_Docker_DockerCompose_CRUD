module.exports = {
    content: [
        "../app/templates/**/*.html",
        "../app/static/js/**/*.js",
        "./tailwind/**/*.css",
        "./frontend/**/*.js",
        "./js/**/*.js"
    ],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
}
