import '../stylesheets/site.scss';

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function(){
        navigator.serviceWorker.register(window.serviceWorkerPath)
        .then(function(reg) {
            console.log('Service worker registered');
        }).catch(function(error) {
            console.error('Service worker not registered: ' + error);
        });
    });
}
