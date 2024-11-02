importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-messaging-compat.js');

const firebaseConfig = {
    apiKey: "AIzaSyCeGqvBeSJhsC-8Eye6rH47W7wA7hIvcOY",
    authDomain: "django-app-69d0f.firebaseapp.com",
    projectId: "django-app-69d0f",
    storageBucket: "django-app-69d0f.appspot.com",
    messagingSenderId: "782742220512",
    appId: "1:782742220512:web:e072e191f35cb4e4692a85"
};

// Firebase ilovasini ishga tushirish
firebase.initializeApp(firebaseConfig);

// Firebase Messaging xizmatini ishga tushirish
const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
    console.log('Background message received: ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/firebase-logo.png'
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
