import '../stylesheets/site.scss';

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(() => {
                console.debug('Service worker registered');
            }).catch((error) => {
                console.error('Service worker not registered: ' + error);
            });
    });
}
