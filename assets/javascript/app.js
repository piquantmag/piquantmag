import '../stylesheets/site.scss';

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function(){
        navigator.serviceWorker.register('/service-worker.js')
        .then(function(reg) {
            console.debug('Service worker registered');
        }).catch(function(error) {
            console.error('Service worker not registered: ' + error);
        });
    });
}
