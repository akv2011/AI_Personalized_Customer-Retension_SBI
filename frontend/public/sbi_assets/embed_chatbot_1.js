SERVER_URL='https://sbilife-chatbot.allincall.in';BOT_ID=1;BOT_NAME='uat';BOT_THEME='2';BOT_POSITION='bottom-right';bot_click_image = 'true';is_form_assist='false';is_lead_generation='false';lead_generation_intent_id='';is_easyassist_enabled='false';easyassist_token='';var web_landing_list=[{'selected_language': 'en', 'data': []}, {'selected_language': 'gu', 'data': '[]'}, {'selected_language': 'kn', 'data': '[]'}, {'selected_language': 'ml', 'data': '[]'}, {'selected_language': 'mr', 'data': '[]'}, {'selected_language': 'pa', 'data': '[]'}, {'selected_language': 'ta', 'data': '[]'}, {'selected_language': 'te', 'data': '[]'}, {'selected_language': 'hi', 'data': '[]'}];notif_and_cross_div = document.createElement('div');notif_and_cross_div.innerHTML ="<div id='notif_and_cross_div' onmouseover='show_cross()' onmouseout='dont_show_cross()' style='position:fixed;right:90px;bottom:7em;height:100px;width:400px;display:none;z-index:9999999999'><svg onclick='hide_notification()' id='cross-chatbox-notification' width='28' height='28' viewBox='0 0 28 28' fill='none' xmlns='http://www.w3.org/2000/svg' style='position: fixed;cursor: pointer;right: 90px;bottom: 12.5em;z-index: 2147483647;display: none;'><circle cx='14' cy='14' r='14' fill='#3871F0' fill-opacity='0.08'></circle><path d='M10.3335 9.21192L14.0001 12.8781L17.6667 9.22303C17.7388 9.14959 17.8255 9.09192 17.9211 9.05367C18.0167 9.01542 18.1193 8.99743 18.2222 9.00084C18.4242 9.01391 18.6145 9.10004 18.7576 9.24315C18.9007 9.38625 18.9869 9.57656 19 9.77852C19.001 9.87782 18.9818 9.97629 18.9436 10.068C18.9054 10.1596 18.849 10.2426 18.7777 10.3118L15.1001 14.0002L18.7777 17.6886C18.9222 17.8286 19.0022 18.0219 19 18.2219C18.9869 18.4239 18.9007 18.6142 18.7576 18.7573C18.6145 18.9004 18.4242 18.9865 18.2222 18.9996C18.1193 19.003 18.0167 18.985 17.9211 18.9468C17.8255 18.9085 17.7388 18.8508 17.6667 18.7774L14.0001 15.1223L10.3446 18.7774C10.2724 18.8508 10.1858 18.9085 10.0902 18.9468C9.99455 18.985 9.89203 19.003 9.78909 18.9996C9.58334 18.9889 9.38886 18.9023 9.24317 18.7567C9.09749 18.611 9.01094 18.4165 9.00023 18.2108C8.99922 18.1115 9.0184 18.013 9.0566 17.9214C9.0948 17.8297 9.15122 17.7467 9.22244 17.6775L12.9001 14.0002L9.21133 10.3118C9.14211 10.2416 9.08775 10.1583 9.05147 10.0666C9.0152 9.97502 8.99777 9.87703 9.00023 9.77852C9.0133 9.57656 9.09944 9.38625 9.24256 9.24315C9.38568 9.10004 9.576 9.01391 9.77798 9.00084C9.88012 8.99599 9.98215 9.01223 10.0777 9.04854C10.1733 9.08486 10.2604 9.14048 10.3335 9.21192V9.21192Z' fill='#3871F0'></path></svg><svg width='351' height='117' viewBox='0 0 351 117' fill='none' xmlns='http://www.w3.org/2000/svg' style='position: fixed;cursor: pointer;right: 80px;bottom: 5em;z-index: 2147483647;display: none;' id='chatbox-notification' onclick='open_up_bot()' class='animate__animated animate__pulse'><g filter='url(#filter0_d)'><rect x='15' y='15' width='321' height='62' rx='31' fill='white'></rect><path d='M298.764 102C298.764 102 270.667 92.1219 268.253 73.243H295.013C288.51 76.7439 282.248 82.7811 298.764 102Z' fill='white'></path></g><defs><filter id='filter0_d' x='0' y='0' width='351' height='117' filterUnits='userSpaceOnUse' color-interpolation-filters='sRGB'><feFlood flood-opacity='0' result='BackgroundImageFix'></feFlood><feColorMatrix in='SourceAlpha' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0'></feColorMatrix><feOffset></feOffset><feGaussianBlur stdDeviation='7.5'></feGaussianBlur><feColorMatrix type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.1 0'></feColorMatrix><feBlend mode='normal' in2='BackgroundImageFix' result='effect1_dropShadow'></feBlend><feBlend mode='normal' in='SourceGraphic' in2='effect1_dropShadow' result='shape'></feBlend></filter></defs><text x='50%' y='40%' dominant-baseline='middle' text-anchor='middle' fill='#4D4D4D' id='prompt-text'></text></svg></div><svg  class='animate__animated animate__fadeIn' id='one-popup-on-bot' width='25' height='25' viewBox='0 0 22 22' fill='none' xmlns='http://www.w3.org/2000/svg' style='position: fixed;cursor: pointer;right: 34px;bottom: 8.3em;z-index: 99999999999999999999;display: none;'><circle cx='11' cy='11' r='11' fill='#E82D2D'></circle><path d='M7.93018 8.85889V7.1084C8.90674 7.1084 9.58789 6.979 9.97363 6.72021C10.3594 6.46143 10.5522 6.05371 10.5522 5.49707H12.7275V16H10.3765V8.85889H7.93018Z' fill='white'></path></svg>";try{document.body.appendChild(notif_and_cross_div);}catch(err){window.onload = () => {document.body.appendChild(notif_and_cross_div)};}var easychat_form_assist_id = ""
var easychat_page_category = ""
var easychat_minimized_chatbot = false
var easychat_do_not_disturb = ""
var easychat_window_location = encodeURIComponent(window.location.href);
var website_cookies = ""
var meta_tags_information = ""
var form_assist_tags = "";
var is_bot_minimized = false
var easychat_intent_name = ""
var is_web_landing_allowed = 'false'
var campaign_link_query_id = "INTENT_ID"
var prompt_message = ""
var chat_bot_maximized = false
var prompt_text_font_family = ""
var auto_popup = null;
var is_bot_loaded = false;
var auto_pop_up_denied = "false";
var count_of_chunk = 0
var total_length_of_chunk = 0
var suggestion_list = []
var db;
var db_name = "suggestion_list"
var table_name = "suggestion_list_table"
var table_index = "suggestion_list_key"
var last_bot_updated_time = 0
var allowed_hosts_list = []
var MAXIMIZE_TEXT = "Click here to maximize"
var MINIMIZE_TEXT = "Click here to minimize"
var initial_trigger_intents = []
var is_initial_trigger_intent = false
var selected_language = "en";
var web_page_source = get_web_page_source()
var welcome_banner_query_question = "INTENT_NAME";
var external_trigger_intent_info = "INTENT_INFO";
var is_voice_based_form_assist_enabled = false;
var popup_enabled = false
var easychat_popup_image
var easychat_popup_min_image
var easychat_popup_close_button
var easychat_popup_minimize
var easychat_popup_minimize_tooltip
var easychat_popup_maximize
var easychat_popup_maximize_tooltip
var web_landing_notification_appended = false;
var is_greeting_bubble_closed = false;
var trigger_intent_pk;
var is_geolocation_enabled = true;

/////////////////////////////// Encryption //////////////////////////

function easychat_set_cookie(cookiename, cookievalue, expiration, path) {

    var secure = "";
    if(window.location.protocol == "https:") {

        secure = "; secure;"
    }

    if (path==""){

        document.cookie = cookiename + "=" + cookievalue+"; expires="+expiration + secure;
    }else{

        document.cookie = cookiename + "=" + cookievalue+"; path="+path+"; expires="+expiration + secure;
    }
}


function custom_encrypt(msgString, key) {
    // msgString is expected to be Utf8 encoded
    var iv = EasyChatCryptoJS.lib.WordArray.random(16);
    var encrypted = EasyChatCryptoJS.AES.encrypt(msgString, EasyChatCryptoJS.enc.Utf8.parse(key), {
        iv: iv
    });
    var return_value = key;
    return_value += "." + encrypted.toString();
    return_value += "." + EasyChatCryptoJS.enc.Base64.stringify(iv);
    return return_value;
}

function generate_random_string(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}


function encrypt_variable(data) {
        
    utf_data = EasyChatCryptoJS.enc.Utf8.parse(data);
    encoded_data = utf_data;
    random_key = generate_random_string(16);
    encrypted_data = custom_encrypt(encoded_data, random_key);

    return encrypted_data;
}


////////////////////////////////////////////////////////////////////////////////////

function get_web_page_source(){
    if(document.referrer != "" && document.referrer != undefined && document.referrer != null){
        return (document.referrer).split('?')[0];
    }
    else{
        return 'direct/(Google)';
    }
}


function show_web_landing_notification(auto_pop_up_text, bot_theme_color, bot_position, easychat_popup_min_image) {
    if(web_landing_notification_appended){
        return;
    }

    var popup_id_and_classes = get_popup_id_and_classes(bot_position)
    var id_popup_wrapper = popup_id_and_classes[0]
    var class_popup_wrapper = popup_id_and_classes[1]
    var class_pop_up_image_wrapper = popup_id_and_classes[2]
    var class_greeting_notification_wrapper = popup_id_and_classes[3]

    var notification_message_div = '<div class="notification-message-div" id="notification-message-div" style="display:none">\
                <div class="notification-message-hide-div" onclick="hide_auto_pop_up_notification_text()">\
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\
                        <circle cx="12" cy="12" r="11.5" fill="white" stroke="#' + bot_theme_color + '"></circle>\
                        <path d="M16.1839 17L12.5029 13.3156L8.82186 17L8 16.1787L11.6868 12.5L8 8.82134L8.82186 8L12.5029 11.6844L16.1839 8.00578L17 8.82134L13.319 12.5L17 16.1787L16.1839 17Z" fill="#' + bot_theme_color + '"></path>\
                    </svg></div>\
                <div class="allincall-notification-message" onclick="open_up_bot()" style="border: 1px solid #' + bot_theme_color + ';">\
                <span> <svg width="28" height="26" viewBox="0 0 28 26" fill="none" xmlns="http://www.w3.org/2000/svg">\
                <path d="M10.8896 17.2108L6.68998 11.8405C6.68998 11.8405 5.86993 10.2885 8.0351 10.1679C8.0351 10.1679 7.07822 8.44705 9.41351 7.95764C9.41351 7.95764 8.39557 6.90729 9.47268 6.15549C10.5498 5.40368 11.3032 6.66714 11.3032 6.66714C11.3032 6.66714 12.6303 4.65722 13.7123 6.04074C14.7942 7.42426 17.3097 10.5104 17.3097 10.5104C17.3097 10.5104 17.5153 7.53379 18.9477 7.22838C20.0809 6.98676 20.3276 7.73942 20.3276 7.73942C20.3276 7.73942 20.6095 10.3757 20.8806 11.4605C21.2576 12.9685 21.2556 14.5389 20.7254 15.5043L22.647 17.9617L16.7544 21.3638L15.0816 19.0005C15.0818 19.0005 12.7019 19.5282 10.8896 17.2108Z" fill="#FFD3B4"></path>\
                <path d="M17.8963 6.8808C17.1904 7.08995 16.6113 7.65362 16.4551 8.28353L16.1311 9.59087L12.8952 5.56503C12.6927 5.30703 12.3692 5.1574 11.9843 5.14364C11.5986 5.12984 11.1972 5.2541 10.8542 5.49353C10.6405 5.64271 10.4701 5.82326 10.3474 6.01718C9.8672 5.46932 8.94834 5.4056 8.26151 5.88506C7.90833 6.1316 7.67143 6.47887 7.59459 6.86288C7.52658 7.20259 7.59313 7.53503 7.78187 7.80679C7.54522 7.86184 7.31348 7.96496 7.10368 8.11143C6.76065 8.35084 6.51703 8.67677 6.41767 9.02913C6.3389 9.30844 6.35864 9.57767 6.47085 9.80635C6.22741 9.8605 5.98852 9.96566 5.77264 10.1163C5.43019 10.3553 5.18626 10.6803 5.08584 11.0312C4.98511 11.3833 5.0407 11.7191 5.24235 11.977L9.81505 17.8243C10.6978 18.9532 12.1727 19.5466 13.8853 19.4695L15.3883 21.6038C15.492 21.751 15.727 21.7759 15.9264 21.6608L21.819 18.2587C21.927 18.1964 22.0091 18.1011 22.0449 17.9967C22.0807 17.8923 22.0667 17.7886 22.0065 17.7116L20.1866 15.3844C20.4727 14.6697 21.1083 12.9046 20.2883 11.2934L19.7904 7.80573C19.7361 7.42552 19.5089 7.11981 19.1507 6.9449C18.7926 6.76999 18.3471 6.74725 17.8963 6.8808ZM18.963 8.04675L19.4676 11.5814C19.4722 11.6132 19.4818 11.6433 19.4964 11.6709C20.2728 13.1475 19.5867 14.8345 19.3612 15.3889L19.3361 15.4508C19.2916 15.5612 19.3031 15.6733 19.3673 15.7552L21.0525 17.9103L15.9379 20.8632L14.5197 18.8493C14.456 18.7587 14.339 18.7111 14.2056 18.7214C12.659 18.8402 11.3203 18.3307 10.5326 17.3235L5.95993 11.4762C5.87205 11.3638 5.8479 11.217 5.89201 11.0629C5.93639 10.9078 6.04444 10.764 6.19621 10.6581C6.34818 10.5521 6.52523 10.4968 6.69515 10.5023C6.86398 10.5078 7.00542 10.5727 7.0933 10.685L9.74996 14.0822C9.87267 14.2391 10.1677 14.2621 10.3765 14.1118C10.5672 13.9745 10.6303 13.741 10.5165 13.5955L7.29516 9.47616C7.20586 9.36194 7.18078 9.21345 7.2246 9.05797C7.26844 8.90253 7.37592 8.75874 7.52727 8.65312C7.67849 8.54754 7.85561 8.49268 8.02576 8.49876C8.19591 8.50485 8.33883 8.57109 8.42813 8.68531L11.6495 12.8047C11.7713 12.9604 12.0325 12.9554 12.2327 12.8155C12.4324 12.676 12.513 12.4416 12.3918 12.2865L8.54056 7.36173C8.42201 7.21013 8.37731 7.02382 8.41469 6.83706C8.44799 6.67097 8.54398 6.52524 8.68514 6.42673C8.99728 6.20882 9.4409 6.27335 9.67364 6.5709L13.5249 11.4957C13.6464 11.651 13.9075 11.6466 14.1074 11.5071C14.3075 11.3674 14.3887 11.133 14.2672 10.9776L11.0457 6.85827C10.8613 6.62248 10.9655 6.25327 11.2779 6.03523C11.4293 5.92957 11.6062 5.87477 11.7764 5.88085C11.9465 5.88693 12.0895 5.95318 12.1788 6.0674L12.181 6.07025L15.8671 10.6562L15.7576 11.0978C15.4527 11.3918 14.6874 12.2258 14.5502 13.3047C14.5245 13.5074 14.689 13.6551 14.9176 13.6346C15.1462 13.6141 15.3525 13.4332 15.3783 13.2304C15.5058 12.2274 16.3781 11.4707 16.3855 11.4643C16.4638 11.3983 16.5185 11.3144 16.5401 11.2274L17.2682 8.28957C17.3475 7.96948 17.6418 7.68302 18.0006 7.57674C18.2296 7.50885 18.456 7.52045 18.638 7.60933C18.82 7.69819 18.9354 7.85357 18.963 8.04675Z" fill="black"></path>\
                <path d="M19.842 3.30215C20.0513 3.18129 20.1445 2.95077 20.0501 2.78727C19.9557 2.62378 19.7095 2.58923 19.5002 2.7101C19.2908 2.83097 19.1976 3.06149 19.292 3.22498C19.3864 3.38847 19.6326 3.42302 19.842 3.30215Z" fill="black"></path>\
                <path d="M14.2341 5.11155C14.2492 5.10001 15.7715 3.95113 17.8577 3.52672C18.0976 3.47788 18.2876 3.25713 18.2646 3.05513C18.244 2.87405 18.0565 2.76504 17.842 2.80864C15.5149 3.28213 13.8422 4.54435 13.7722 4.59783C13.5806 4.74408 13.5288 4.9776 13.6564 5.11947C13.784 5.26134 14.0426 5.25769 14.2341 5.11155Z" fill="black"></path>\
                <path d="M15.3205 5.2931C15.1184 5.42546 15.0433 5.65761 15.152 5.81233C15.2608 5.96707 15.5132 5.9857 15.7159 5.85382C15.7358 5.841 17.7198 4.57136 19.9704 4.80634C20.201 4.83039 20.455 4.65935 20.5096 4.44422C20.557 4.25715 20.4367 4.09407 20.2365 4.07319C17.6329 3.80134 15.4137 5.23209 15.3205 5.2931Z" fill="black"></path>\
                <path d="M5.53285 14.7613C5.66201 14.5728 5.61311 14.3581 5.42338 14.2814C5.23337 14.2046 4.97403 14.2954 4.84429 14.484C4.80817 14.5365 3.95937 15.7869 3.90517 17.3235C3.89866 17.5078 4.05843 17.6399 4.26837 17.6241C4.50946 17.6059 4.73067 17.4008 4.73814 17.1897C4.78459 15.873 5.52539 14.7723 5.53285 14.7613Z" fill="black"></path>\
                <path d="M5.89352 16.0002C5.87206 16.0523 5.37051 17.2913 5.59341 18.5169C5.62661 18.6995 5.83239 18.7977 6.0518 18.7352C6.28372 18.6691 6.45236 18.4472 6.41726 18.2542C6.22897 17.2189 6.66503 16.1289 6.67124 16.1137C6.75364 15.9126 6.64679 15.7242 6.4323 15.6927C6.21749 15.6613 5.97627 15.7989 5.89352 16.0002Z" fill="black"></path>\
            </svg></span><span class="notification-message-sub-div" style="font-family:' + prompt_text_font_family + '"> '+ auto_pop_up_text+'</span></div></div>'
    notification_counter='<div class="allincall-notification-div" onclick="open_up_bot()" id="allincall-notification-count" style="display:none">1</div>'
    if(document.getElementsByClassName('allincall-popup-image-icon-wrapper')[0]){
        wrapper_html = '<div class="' + class_greeting_notification_wrapper + '">' 
        html = wrapper_html + notification_message_div + '</div>' + notification_counter
        document.getElementsByClassName('allincall-popup-image-icon-wrapper')[0].insertAdjacentHTML('beforeend', html)
        web_landing_notification_appended = true;
        return;
    }
    wrapper_html = '<div id="' + id_popup_wrapper + '" class="' + class_popup_wrapper + '"><div class="' + class_pop_up_image_wrapper + '"><div class="' + class_greeting_notification_wrapper + '">'  
    notification_message_div_element = document.createElement("div");
    notification_message_div_element.setAttribute("easyassist_avoid_sync", "true")
     // changed code
                notification_message_div_element.innerHTML += wrapper_html + notification_message_div  + '</div></div></div>';                
    // end changed code

    notification_counter_element = document.createElement("div");
    notification_counter_element.innerHTML += notification_counter;
    // document.body.appendChild(notification_counter_element)
    document.body.appendChild( notification_message_div_element)

    var easychat_popup_image_div = ''
    if (is_minimization_enabled) {

        easychat_popup_image_div += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML + easychat_popup_min_image.outerHTML +
                                              easychat_popup_minimize.outerHTML + easychat_popup_maximize.outerHTML

        document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(notification_counter_element)
        document.getElementsByClassName(class_pop_up_image_wrapper)[0].innerHTML += easychat_popup_image_div

        document.getElementById("allincall-minimize-popup").appendChild(easychat_popup_minimize_tooltip)
        document.getElementById("allincall-maximize-popup").appendChild(easychat_popup_maximize_tooltip)
    } else {
        easychat_popup_image_div += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML

        document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(notification_counter_element)
        document.getElementsByClassName(class_pop_up_image_wrapper)[0].innerHTML += easychat_popup_image_div

    }
    web_landing_notification_appended = true;
}

// easychat-bot-unread-message
function show_web_landing_intents(bot_theme_color, bot_position, easychat_popup_min_image) {
    
    if (is_auto_pop_allowed_desktop || is_auto_pop_allowed_mobile || is_form_assist_auto_pop_allowed){
        return
        // no need to show web_landing in case of form assist is enabled or auto pop up is enabled
    }
    if(is_minimization_enabled && window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') == 'true'){
        return
    }

    var current_url = window.location.href;
    try {
        if(web_landing_list.length > 0) {

            for(var i = 0; i < web_landing_list.length; i++) {

                if(selected_language == web_landing_list[i]["selected_language"]) {
                   try{
                        web_landing_list = JSON.parse(web_landing_list[i]["data"]);
                    }catch(err){
                        console.log(err);
                        web_landing_list = web_landing_list[i]["data"];
                    }
                    break;
                }
            }
        }
        if (web_landing_list.length > 0) {
            for (var i = 0; i < web_landing_list.length; i++) {
                url = web_landing_list[i]["url"]
                intent_name = web_landing_list[i]["intent_name"]
                trigger_intent_pk = web_landing_list[i]["trigger_intent_pk"]
                if (url == current_url) {
                    popup_enabled = true

                    easychat_intent_name = intent_name;
                    is_web_landing_allowed = 'true';
                    try {
                        if (web_landing_list[i]["show_prompt_message_after_timer"] == 'true') {
                            prompt_message = web_landing_list[i]["prompt_message"];
                            show_web_landing_notification(prompt_message, bot_theme_color, bot_position, easychat_popup_min_image);
                            
                            prompt_message_timer = parseInt(web_landing_list[i]["prompt_message_timer"]) * 1000;
                            setTimeout(function(e) {
                                if (chat_bot_maximized == false || (window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') != 'true' && !easychat_minimized_chatbot)) {
                                    setTimeout(function(e) {
                                        if(window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') == 'true'){
                                            return
                                        }
                                            document.getElementById("allincall-notification-count").style.display="flex"
                                            document.getElementById("notification-message-div").style.display="block"
                                            if(BOT_POSITION.indexOf("top") != -1 && document.getElementById("notification-message-div").parentNode.className.indexOf("greeting") != -1) {
                                                document.getElementById("notification-message-div").style.display="flex"
                                            }
                                        }, 800)
                                }
                            }, prompt_message_timer);
                        }
                    } catch (err) { console.log(err) }
                }
            }
        }
    } catch (err) {}
}

function check_campaign_link() {
    var campaign_link_intent = easychat_get_url_vars()["easychat_query"]
    if (campaign_link_intent != undefined && campaign_link_intent != "" && campaign_link_intent != null) {
        campaign_link_query_id = campaign_link_intent
        if(window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') == 'true') return;
        document.getElementById("allincall-popup").click();
    }
}

function check_welcome_banner_question() {
    var query_question = easychat_get_url_vars()["query_question"];
    if (query_question != undefined && query_question != "" && query_question != null) {
        welcome_banner_query_question = query_question;
        document.getElementById("allincall-popup").click()
    }
}

function check_auto_popup(){

    let bot_minimized_state = get_cookie("is_bot_minimized");
    let is_auto_popup_required = get_cookie("is_auto_popup_required");

    if(is_greeting_bubble_closed) return;

    if(is_auto_popup_required == "false") return;

    if(bot_minimized_state != 'true') {
        auto_pop_up_denied = get_cookie("auto_pop_up_denied");

        var isMobile = (('ontouchstart' in document.documentElement && (/mobi/i.test(navigator.userAgent))) || (navigator.userAgent.match(/(iPad)/) || (navigator.platform === 'MacIntel' && typeof navigator.standalone !== "undefined")));
        
        if(isMobile){
            if (is_auto_pop_allowed_mobile == true && is_form_assist_auto_pop_allowed == false && auto_pop_up_denied != "true"  && correct_path_of_bot_for_autopopup() == true) {
    
                if (!is_auto_popup_inactivity_enabled) {
                    trigger_autopopup_functionality(auto_pop_up_timer, auto_popup_type)
                }  else {                    
                    auto_popup_inactivity_detector(auto_pop_up_timer, auto_popup_type)
                }
            }
        }
        else{
            if (is_auto_pop_allowed_desktop == true && is_form_assist_auto_pop_allowed == false && auto_pop_up_denied != "true"  && correct_path_of_bot_for_autopopup() == true) {
                
                if (!is_auto_popup_inactivity_enabled) {                   
                    trigger_autopopup_functionality(auto_pop_up_timer, auto_popup_type)
                } else {                    
                    auto_popup_inactivity_detector(auto_pop_up_timer, auto_popup_type)
                }
            }                
        }
    }
}

function check_and_change_state_of_bot(){
    if(window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') == 'true'){
        document.getElementById("allincall-popup").style.display = "none";
        document.getElementById("allincall-min-popup").style.display = "block";
        document.getElementById("allincall-maximize-popup").style.display = "flex";
        document.getElementById("allincall-minimize-popup").style.display = "none";
        document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
        document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";

        change_css_on_bot_minimization(BOT_POSITION)
    } else {
        document.getElementById("allincall-popup").style.display = "block";
        document.getElementById("allincall-min-popup").style.display = "none";
        document.getElementById("allincall-maximize-popup").style.display = "none";
        document.getElementById("allincall-minimize-popup").style.display = "";
        document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
        document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";

        change_css_on_bot_maximization(BOT_POSITION)
    }
}


// Get Webiste Cookies
function getCookies() {
    var pairs = document.cookie.split(";");
    var cookies = {};
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split("=");
        cookies[(pair[0] + '').trim()] = unescape(pair.slice(1).join('='));
    }
    return cookies;
}

function get_cookie(cookiename) {
    var cookie_name = cookiename + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookie_array = decodedCookie.split(';');
    for (var i = 0; i < cookie_array.length; i++) {
        var c = cookie_array[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(cookie_name) == 0) {
            return c.substring(cookie_name.length, c.length);
        }
    }
    return "";
}

// Get Webiste META Data
var meta_tag_filter_list = ["title", "description", "keywords"];

function get_meta_tag_information() {
    var meta_tags = document.getElementsByTagName("meta");
    var meta_tag_dict = {};
    for (var index = 0; index < meta_tags.length; index++) {
        var meta_tag_name = meta_tags[index].getAttribute("name");
        for (var m_index = 0; m_index < meta_tag_filter_list.length; m_index++) {
            if (meta_tag_name == meta_tag_filter_list[m_index]) {
                meta_tag_dict[meta_tag_name] = meta_tags[index].getAttribute("content");
            }
        }
    }
    return meta_tag_dict;
}




// Include CSS files
function easychat_add_css(filename) {
    var head = document.getElementsByTagName('head')[0];
    var style = document.createElement('link');
    style.href = filename;
    style.type = 'text/css';
    style.rel = 'stylesheet';
    document.head.appendChild(style);
}

// Include script files
function easychat_add_script(filename) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.src = filename;
    script.type = 'text/javascript';
    document.head.appendChild(script)
}

if( document.readyState !== 'loading' ) {
    initialize_easychat_bot();
} else  {
    document.addEventListener("DOMContentLoaded", function(event) {
        initialize_easychat_bot();
    });    
}

function initialize_easychat_bot() {
    easychat_add_css(SERVER_URL + "/static/EasyChatApp/css/embed.css");
    easychat_add_css(SERVER_URL + "/static/EasyChatApp/css/theme2_embed.css");
    easychat_add_css(SERVER_URL + "/static/EasyChatApp/css/themes_popup.css");
    //easychat_add_css(SERVER_URL + "/static/EasyChatApp/font-awesome-4.7.0/css/font-awesome.min.css");
    easychat_add_script(SERVER_URL + "/static/EasyChatApp/js/easychat-crypto.js");
    easychat_add_css(SERVER_URL + "/static/EasyChatApp/css/animate.css");    

    setTimeout(function() {
        load_easychat_bot();
    }, 300)
}

function get_form_assist_tags() {
    var xhttp = new XMLHttpRequest();
    var params = '&bot_id=' + BOT_ID;
    xhttp.open("POST", SERVER_URL + "/chat/get-form-assist-tags/", true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
            if (response["status"] == 200) {
                window.form_assist_tags = response["form_assist_tags"];
            }
        }
    }
    xhttp.send(params);

}


// Import form assist code when form assist is allowed
if (is_form_assist == "true") {
    easychat_add_script(SERVER_URL + "/static/EasyChatApp/js/form_assist.js");
    get_form_assist_tags();
}

if (is_easyassist_enabled == "true") {
    easychat_add_script(SERVER_URL + "/static/EasyAssistApp/js/easy-assist-v6.js?key=" + easyassist_token);
}

// var slideIndex = 1;

function easychat_get_url_vars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m, key, value) {
        vars[key] = value;
    });
    return vars;
}

// On windows loads
// window.onload = function() {
//     load_easychat_bot();
// }
function set_easychat_selected_language(language) {

    // Setting default language English(en)
    if(window.localStorage['selected_language'] == null || window.localStorage['selected_language'] == undefined) {

        window.localStorage['selected_language'] = language;
    } else {

        selected_language = window.localStorage['selected_language'];
    }
}

function get_easychat_selected_language() {

    // Setting default language English(en)
    if(window.localStorage['selected_language'] == null || window.localStorage['selected_language'] == undefined) {

        return selected_language
    } else {

        selected_language = window.localStorage['selected_language'];
        return selected_language
    }
}


function auto_popup_inactivity_detector(auto_pop_up_timer, auto_popup_type) {
    var idleTime = 0;
    var bot_triggered = false;
    
        // Increment the idle time counter every minute.
        var idleInterval = setInterval(timerIncrement, 1000); // 1 sec

        // Zero the idle timer on user movement.
        window.onscroll = function(e) {
            idleTime = 0;
        }

        document.onscroll = document.onkeypress = document.onmousemove = document.mousedown = document.mouseup = document.onkeydown = document.onkeyup = document.focus = function(){
            idleTime = 0;
        };
    
    function timerIncrement() {
        idleTime = idleTime + 1
        if(idleTime > auto_pop_up_timer && !bot_triggered)
        {
            trigger_autopopup_functionality(0.5, auto_popup_type)
            bot_triggered = true
            clearInterval(idleInterval)

        }
    }
}

function load_easychat_bot() {
    if (is_bot_loaded) return;

    try {
        if (lead_generation_intent_id == undefined || lead_generation_intent_id == null) {
            lead_generation_intent_id = '';
        }
    } catch {
        lead_generation_intent_id = '';
    }

    set_easychat_selected_language(selected_language);
    is_bot_loaded = true;
    if (is_lead_generation == 'true') {
        is_form_assist = 'false'
    }
    try {
        website_cookies = getCookies()
        website_cookies = JSON.stringify(website_cookies)
        website_cookies = encrypt_variable(website_cookies)

        meta_tags_information = get_meta_tag_information()
        meta_tags_information = JSON.stringify(meta_tags_information)
        meta_tags_information = encrypt_variable(meta_tags_information)
    } catch (err) {
        console.log(err)
    }
    //If form asssit is true call form assist function in form_assist.js

    var easychat_iframe = document.createElement('iframe');
    easychat_iframe.style.display = "none";
    easychat_iframe.id = "allincall-chat-box";
    easychat_iframe.frameborder = "0";
    easychat_iframe.zIndex = "2147483647";
    easychat_iframe.backgroundColor = "transparent";
    easychat_iframe.allow = "microphone; geolocation;";
    easychat_iframe.setAttribute("easyassist_avoid_sync", "true");

    document.body.appendChild(easychat_iframe);

    url_parameters = easychat_get_url_vars();
    var xhttp = new XMLHttpRequest();
    var json_string = JSON.stringify({
        bot_id: BOT_ID,
        web_page: window.location.href,
        selected_language: selected_language,
        web_page_source: web_page_source
    })
    json_string = encodeURIComponent(json_string)
    var params = 'json_string=' + json_string;
    xhttp.open("POST", SERVER_URL + "/chat/get-bot-image/", true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);

            selected_language = response.selected_language;
            MINIMIZE_TEXT = response.minimize_text
            MAXIMIZE_TEXT = response.maximize_text
            prompt_text_font_family = response.font_style;
            prompt_text_family_to_pass_in_google_api = prompt_text_font_family.replace(" ", '+')
            last_bot_updated_time = response.last_bot_updated_time
            window.disable_auto_popup_minimized = response.disable_auto_popup_minimized
            is_geolocation_enabled = response.is_geolocation_enabled;
            // if(get_cookie('last_bot_updated_time') != last_bot_updated_time){
            //     load_storage();
            //     get_suggestions();
            // }
            // easychat_set_cookie("last_bot_updated_time",last_bot_updated_time,"","")
            easychat_add_css("https://fonts.googleapis.com/css?family=" + prompt_text_family_to_pass_in_google_api)
            allowed_hosts_list = response["allowed_hosts"]
            var bot_theme_color = response.bot_theme_color
            var bot_theme_light_color = response.bot_theme_light_color

            easychat_popup_image = document.createElement("img");
            initial_trigger_intents = JSON.parse(response["auto_popup_initial_messages"]);
            easychat_popup_image.id = "allincall-popup";
            easychat_popup_image.style.position = "fixed";
            easychat_popup_image.style.cursor = "pointer";
            easychat_popup_image.style.right = "20px";
            easychat_popup_image.style.bottom = "0em";
            easychat_popup_image.style.width = "8em";
            easychat_popup_image.style.zIndex = "2147483647";
            easychat_popup_image.setAttribute("easyassist_avoid_sync", "true");

            // var easychat_popup_span = document.createElement("span");
                easychat_popup_close_button = document.createElement("span");
                easychat_popup_close_button.id = "easychat-bot-close-button";
                // easychat_popup_close_button.src ="/static/EasyChatApp/img/cancel5.png";
                easychat_popup_close_button.style.backgroundColor = "#" + bot_theme_color;
                easychat_popup_close_button.style.display ="none";
                easychat_popup_close_button.style.position = "fixed";
                easychat_popup_close_button.style.cursor = "pointer";
                easychat_popup_close_button.style.right = "40px";
                easychat_popup_close_button.style.bottom = "0.5em";
                easychat_popup_close_button.style.width = "2.5em";
                easychat_popup_close_button.style.boxShadow = "0px 2px 12px " + bot_theme_light_color + "";
                easychat_popup_close_button.setAttribute("easyassist_avoid_sync", "true");
                // easychat_popup_close_button.style.zIndex = "2147483647";

                var bot_close_icon_fill_color = "white";
                if (bot_theme_color.toLowerCase() == "ffffff") {
                    bot_close_icon_fill_color = "#767B87";
                }
                
                easychat_popup_close_button.innerHTML='<svg width="14" style="margin-top: 13px;" height="14" viewBox="0 0 14 14" fill="' + bot_close_icon_fill_color + '" xmlns="http://www.w3.org/2000/svg">\
                    <path d="M12.7305 14L7.0045 8.26864L1.27846 14L0 12.7224L5.73505 7L0 1.27763L1.27846 0L7.0045 5.73136L12.7305 0.00899763L14 1.27763L8.27396 7L14 12.7224L12.7305 14Z" fill="' + bot_close_icon_fill_color + '"/>\
                </svg>'
                
            is_minimization_enabled = response.is_minimization_enabled
            if (is_minimization_enabled) {
                easychat_popup_min_image = document.createElement("img");
                easychat_popup_min_image.id = "allincall-min-popup";
                easychat_popup_min_image.style.position = "fixed";
                easychat_popup_min_image.style.cursor = "pointer";
                easychat_popup_min_image.style.right = "21px";
                easychat_popup_min_image.style.bottom = "5em";
                easychat_popup_min_image.style.width = "54px";
                easychat_popup_min_image.style.zIndex = "2147483647";
                easychat_popup_min_image.style.display = "none";
                easychat_popup_min_image.setAttribute("easyassist_avoid_sync", "true");

                easychat_popup_minimize = document.createElement("span");
                easychat_popup_minimize.id = "allincall-minimize-popup";
                easychat_popup_minimize.innerHTML = '<svg width="12" height="12" viewBox="0 0 12 12" fill="#7B7A7B" xmlns="http://www.w3.org/2000/svg">\
                                                        <path d="M5.99997 8.30913C6.2037 8.30939 6.39766 8.22188 6.5323 8.06898L9.55296 4.63607C9.69278 4.48436 9.73947 4.26882 9.67496 4.07285C9.61044 3.87688 9.44484 3.73122 9.24224 3.69225C9.03963 3.65327 8.83181 3.72709 8.69919 3.88514L6.05785 6.88702C6.04323 6.90369 6.02214 6.91325 5.99997 6.91325C5.97779 6.91325 5.9567 6.90369 5.94208 6.88702L3.30074 3.88452C3.16812 3.72648 2.9603 3.65266 2.7577 3.69163C2.55509 3.73061 2.38949 3.87626 2.32498 4.07223C2.26046 4.2682 2.30715 4.48375 2.44698 4.63546L5.46671 8.06775C5.60158 8.22102 5.79581 8.30894 5.99997 8.30913Z" />\
                                                        <mask id="mask0_22_172" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="2" y="3" width="8" height="6">\
                                                        <path d="M5.99997 8.30913C6.2037 8.30939 6.39766 8.22188 6.5323 8.06898L9.55296 4.63607C9.69278 4.48436 9.73947 4.26882 9.67496 4.07285C9.61044 3.87688 9.44484 3.73122 9.24224 3.69225C9.03963 3.65327 8.83181 3.72709 8.69919 3.88514L6.05785 6.88702C6.04323 6.90369 6.02214 6.91325 5.99997 6.91325C5.97779 6.91325 5.9567 6.90369 5.94208 6.88702L3.30074 3.88452C3.16812 3.72648 2.9603 3.65266 2.7577 3.69163C2.55509 3.73061 2.38949 3.87626 2.32498 4.07223C2.26046 4.2682 2.30715 4.48375 2.44698 4.63546L5.46671 8.06775C5.60158 8.22102 5.79581 8.30894 5.99997 8.30913Z" fill="white"/>\
                                                        </mask>\
                                                        <g mask="url(#mask0_22_172)">\
                                                        </g>\
                                                    </svg>'
                                                                                        

                easychat_popup_minimize_tooltip = document.createElement("span");
                easychat_popup_minimize_tooltip.id = "allincall-minimize-popup-tooltip";
                easychat_popup_minimize_tooltip.textContent = MINIMIZE_TEXT;
                easychat_popup_minimize_tooltip.style.visibiity = "hidden";
                easychat_popup_minimize_tooltip.style.fontFamily = prompt_text_font_family;
                easychat_popup_minimize_tooltip.style.backgroundColor = bot_theme_light_color;

                easychat_popup_maximize = document.createElement("span");
                easychat_popup_maximize.id = "allincall-maximize-popup";
                easychat_popup_maximize.innerHTML = '<svg width="8" height="9" viewBox="0 0 8 9" fill="#7B7A7B" xmlns="http://www.w3.org/2000/svg">\
                                                        <path d="M4.19989 2.5836C4.34249 2.58343 4.47827 2.64468 4.57252 2.75171L6.68698 5.15475C6.78486 5.26094 6.81754 5.41182 6.77238 5.549C6.72722 5.68618 6.6113 5.78814 6.46947 5.81542C6.32765 5.84271 6.18218 5.79103 6.08934 5.6804L4.2404 3.57909C4.23017 3.56742 4.21541 3.56072 4.19989 3.56072C4.18436 3.56072 4.1696 3.56742 4.15937 3.57909L2.31043 5.68083C2.21759 5.79146 2.07212 5.84314 1.9303 5.81586C1.78847 5.78857 1.67255 5.68662 1.62739 5.54943C1.58223 5.41225 1.61491 5.26137 1.71279 5.15518L3.82661 2.75257C3.92101 2.64528 4.05697 2.58374 4.19989 2.5836Z"/>\
                                                        <mask id="mask0_22_153" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="1" y="2" width="6" height="4">\
                                                        <path d="M4.19989 2.5836C4.34249 2.58343 4.47827 2.64468 4.57252 2.75171L6.68698 5.15475C6.78486 5.26094 6.81754 5.41182 6.77238 5.549C6.72722 5.68618 6.6113 5.78814 6.46947 5.81542C6.32765 5.84271 6.18218 5.79103 6.08934 5.6804L4.2404 3.57909C4.23017 3.56742 4.21541 3.56072 4.19989 3.56072C4.18436 3.56072 4.1696 3.56742 4.15937 3.57909L2.31043 5.68083C2.21759 5.79146 2.07212 5.84314 1.9303 5.81586C1.78847 5.78857 1.67255 5.68662 1.62739 5.54943C1.58223 5.41225 1.61491 5.26137 1.71279 5.15518L3.82661 2.75257C3.92101 2.64528 4.05697 2.58374 4.19989 2.5836Z" fill="white"/>\
                                                        </mask>\
                                                        <g mask="url(#mask0_22_153)">\
                                                        </g>\
                                                    </svg>'

                easychat_popup_maximize_tooltip = document.createElement("span");
                easychat_popup_maximize_tooltip.id = "allincall-maximize-popup-tooltip";
                easychat_popup_maximize_tooltip.textContent = MAXIMIZE_TEXT;
                easychat_popup_maximize_tooltip.style.visibiity = "hidden";
                easychat_popup_maximize_tooltip.style.fontFamily = prompt_text_font_family;
                easychat_popup_maximize_tooltip.style.backgroundColor = bot_theme_light_color;

                

            } else {
                easychat_popup_min_image = "None"
            }

            response = JSON.parse(this.responseText);

            if (BOT_POSITION.indexOf("right") != -1) {
                easychat_popup_image.style.right = "20px";
                if (is_minimization_enabled) {
                    easychat_popup_min_image.style.right = "20px";
                }
                if (BOT_POSITION.indexOf("top") != -1) {
                    easychat_popup_image.style.top = "0px";

                    if (is_minimization_enabled) {
                        easychat_popup_min_image.style.top = "0em";

                        easychat_popup_minimize.style.top = "20px";
                        easychat_popup_minimize_tooltip.style.bottom = "unset";
                        easychat_popup_minimize_tooltip.style.top = "40px";
                        easychat_popup_minimize_tooltip.style.right = "158px";

                        easychat_popup_maximize.style.top = "5px";
                        easychat_popup_maximize_tooltip.style.bottom = "unset";

                        easychat_popup_maximize_tooltip.style.top = "22px";
                        easychat_popup_maximize_tooltip.style.right = "87px";
                    }
                } else {
                    if (is_minimization_enabled) {
                        easychat_popup_min_image.style.bottom = "1em";

                        easychat_popup_maximize.style.bottom = "60px";
                        easychat_popup_minimize_tooltip.style.right = "154px";
                        easychat_popup_minimize_tooltip.style.bottom = "107px";
                        easychat_popup_maximize_tooltip.style.right = "83px";
                        easychat_popup_maximize_tooltip.style.bottom = "68px";
                    }
                }
            } else {
                easychat_popup_image.style.left = "20px";
                easychat_popup_close_button.style.left= "380px";
                
                if (is_minimization_enabled) {
                    easychat_popup_min_image.style.left = "20px";

                    easychat_popup_minimize.style.left = "150px";
                    easychat_popup_minimize_tooltip.style.left = "175px";

                    easychat_popup_maximize.style.left = "65px";
                    easychat_popup_maximize_tooltip.style.left = "85px";

                    easychat_popup_minimize_tooltip.style.right = "unset";
                    easychat_popup_maximize_tooltip.style.right = "unset";
                }
                if (BOT_POSITION.indexOf("top") != -1) {
                    easychat_popup_image.style.top = "0px";
                    if (is_minimization_enabled) {
                        easychat_popup_min_image.style.top = "0em";

                        easychat_popup_minimize.style.top = "20px";

                        easychat_popup_minimize_tooltip.style.top = "45px";
                        easychat_popup_minimize_tooltip.style.bottom = "unset";

                        easychat_popup_maximize.style.top = "5px";
                        easychat_popup_maximize_tooltip.style.top = "22px";
                        easychat_popup_maximize_tooltip.style.bottom = "unset";
                    }
                } else {
                    if (is_minimization_enabled) {
                        easychat_popup_min_image.style.bottom = "1em";

                        easychat_popup_maximize.style.bottom = "60px";
                        easychat_popup_maximize_tooltip.style.bottom = "68px";
                    }
                }
            }

            window.form_assist_autopop_up_timer = response.form_assist_autopop_up_timer;
            window.form_assist_inactivity_timer = response.form_assist_inactivity_timer;
            window.is_auto_pop_allowed = response.is_auto_pop_allowed;
            window.is_auto_pop_allowed_mobile = response.is_auto_pop_allowed_mobile;
            window.is_auto_pop_allowed_desktop = response.is_auto_pop_allowed_desktop;
            window.is_auto_popup_inactivity_enabled = response.is_auto_popup_inactivity_enabled;
            window.auto_popup_type = response.auto_popup_type;
            window.auto_pop_up_timer = response.auto_pop_timer
            window.auto_pop_up_text = response.auto_pop_text
            window.is_form_assist_auto_pop_allowed = response.is_form_assist_auto_pop_allowed
            window.is_nps_required = response.is_nps_required
            window.form_assist_auto_popup_type = response.form_assist_auto_popup_type;
            window.form_assist_intent_bubble_timer = response.form_assist_intent_bubble_timer;
            window.form_assist_intent_bubble_inactivity_timer = response.form_assist_intent_bubble_inactivity_timer;
            window.form_assist_intent_bubble_type = response.form_assist_intent_bubble_type;
            window.form_assist_auto_pop_text = response.form_assist_auto_pop_text;
            window.form_assist_intent_bubble = JSON.parse(response.form_assist_intent_bubble);
            window.form_assist_tag_timer = JSON.parse(response.form_assist_tag_timer);
            window.voice_based_form_assist_enabled = response.is_voice_based_form_assist_enabled;
            window.form_assist_intent_responses_dict = JSON.parse(response.form_assist_intent_responses_dict);
            window.enable_response_form_assist = response.enable_response_form_assist
            window.form_assist_tag_intents = JSON.parse(response.form_assist_tag_intents)
            window.form_assist_tag_mapping = JSON.parse(response.form_assist_tag_mapping)
            window.localStorage['autocorrect_bot_replace'] = JSON.stringify(response['autocorrect_bot_replace'])

             // changed code

            if (response.status == 200 && response.bot_image_url != "") {
                easychat_popup_image.src = SERVER_URL + response.bot_image_url;
                if (is_minimization_enabled) {
                    easychat_popup_min_image.src = SERVER_URL + response.bot_image_url;
                }

            } else {
                easychat_popup_image.src = SERVER_URL + "/static/EasyChatApp/img/popup-4.gif";
                if (is_minimization_enabled) {
                    easychat_popup_min_image.src = SERVER_URL + "/static/EasyChatApp/img/popup-4.gif";
                }
            }

             var popup_id_and_classes = get_popup_id_and_classes(BOT_POSITION)
             var id_popup_wrapper = popup_id_and_classes[0]
             var class_popup_wrapper = popup_id_and_classes[1]
             var class_pop_up_image_wrapper = popup_id_and_classes[2]
             var class_greeting_notification_wrapper = popup_id_and_classes[3]

                // changed code ended
            
            if(auto_popup_type == "2" && !is_form_assist_auto_pop_allowed){

            popup_enabled = true
            wrapper_html = '<div id="' + id_popup_wrapper + '" class="' + class_popup_wrapper + '"><div class="' + class_pop_up_image_wrapper + '"><div class="' + class_greeting_notification_wrapper + '">'  

             notification_message_div = '<div class="notification-message-div" style="display:none;" id="notification-message-div">\
                <div class="notification-message-hide-div" onclick="hide_auto_pop_up_notification_text()">\
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\
                        <circle cx="12" cy="12" r="11.5" fill="white" stroke="#' + bot_theme_color + '"></circle>\
                        <path d="M16.1839 17L12.5029 13.3156L8.82186 17L8 16.1787L11.6868 12.5L8 8.82134L8.82186 8L12.5029 11.6844L16.1839 8.00578L17 8.82134L13.319 12.5L17 16.1787L16.1839 17Z" fill="#' + bot_theme_color + '"></path>\
                    </svg></div>\
                <div class="allincall-notification-message" onclick="open_up_bot_by_greeting()" style="border: 1px solid #' + bot_theme_color + ';">\
                <span> <svg width="28" height="26" viewBox="0 0 28 26" fill="none" xmlns="http://www.w3.org/2000/svg">\
                <path d="M10.8896 17.2108L6.68998 11.8405C6.68998 11.8405 5.86993 10.2885 8.0351 10.1679C8.0351 10.1679 7.07822 8.44705 9.41351 7.95764C9.41351 7.95764 8.39557 6.90729 9.47268 6.15549C10.5498 5.40368 11.3032 6.66714 11.3032 6.66714C11.3032 6.66714 12.6303 4.65722 13.7123 6.04074C14.7942 7.42426 17.3097 10.5104 17.3097 10.5104C17.3097 10.5104 17.5153 7.53379 18.9477 7.22838C20.0809 6.98676 20.3276 7.73942 20.3276 7.73942C20.3276 7.73942 20.6095 10.3757 20.8806 11.4605C21.2576 12.9685 21.2556 14.5389 20.7254 15.5043L22.647 17.9617L16.7544 21.3638L15.0816 19.0005C15.0818 19.0005 12.7019 19.5282 10.8896 17.2108Z" fill="#FFD3B4"></path>\
                <path d="M17.8963 6.8808C17.1904 7.08995 16.6113 7.65362 16.4551 8.28353L16.1311 9.59087L12.8952 5.56503C12.6927 5.30703 12.3692 5.1574 11.9843 5.14364C11.5986 5.12984 11.1972 5.2541 10.8542 5.49353C10.6405 5.64271 10.4701 5.82326 10.3474 6.01718C9.8672 5.46932 8.94834 5.4056 8.26151 5.88506C7.90833 6.1316 7.67143 6.47887 7.59459 6.86288C7.52658 7.20259 7.59313 7.53503 7.78187 7.80679C7.54522 7.86184 7.31348 7.96496 7.10368 8.11143C6.76065 8.35084 6.51703 8.67677 6.41767 9.02913C6.3389 9.30844 6.35864 9.57767 6.47085 9.80635C6.22741 9.8605 5.98852 9.96566 5.77264 10.1163C5.43019 10.3553 5.18626 10.6803 5.08584 11.0312C4.98511 11.3833 5.0407 11.7191 5.24235 11.977L9.81505 17.8243C10.6978 18.9532 12.1727 19.5466 13.8853 19.4695L15.3883 21.6038C15.492 21.751 15.727 21.7759 15.9264 21.6608L21.819 18.2587C21.927 18.1964 22.0091 18.1011 22.0449 17.9967C22.0807 17.8923 22.0667 17.7886 22.0065 17.7116L20.1866 15.3844C20.4727 14.6697 21.1083 12.9046 20.2883 11.2934L19.7904 7.80573C19.7361 7.42552 19.5089 7.11981 19.1507 6.9449C18.7926 6.76999 18.3471 6.74725 17.8963 6.8808ZM18.963 8.04675L19.4676 11.5814C19.4722 11.6132 19.4818 11.6433 19.4964 11.6709C20.2728 13.1475 19.5867 14.8345 19.3612 15.3889L19.3361 15.4508C19.2916 15.5612 19.3031 15.6733 19.3673 15.7552L21.0525 17.9103L15.9379 20.8632L14.5197 18.8493C14.456 18.7587 14.339 18.7111 14.2056 18.7214C12.659 18.8402 11.3203 18.3307 10.5326 17.3235L5.95993 11.4762C5.87205 11.3638 5.8479 11.217 5.89201 11.0629C5.93639 10.9078 6.04444 10.764 6.19621 10.6581C6.34818 10.5521 6.52523 10.4968 6.69515 10.5023C6.86398 10.5078 7.00542 10.5727 7.0933 10.685L9.74996 14.0822C9.87267 14.2391 10.1677 14.2621 10.3765 14.1118C10.5672 13.9745 10.6303 13.741 10.5165 13.5955L7.29516 9.47616C7.20586 9.36194 7.18078 9.21345 7.2246 9.05797C7.26844 8.90253 7.37592 8.75874 7.52727 8.65312C7.67849 8.54754 7.85561 8.49268 8.02576 8.49876C8.19591 8.50485 8.33883 8.57109 8.42813 8.68531L11.6495 12.8047C11.7713 12.9604 12.0325 12.9554 12.2327 12.8155C12.4324 12.676 12.513 12.4416 12.3918 12.2865L8.54056 7.36173C8.42201 7.21013 8.37731 7.02382 8.41469 6.83706C8.44799 6.67097 8.54398 6.52524 8.68514 6.42673C8.99728 6.20882 9.4409 6.27335 9.67364 6.5709L13.5249 11.4957C13.6464 11.651 13.9075 11.6466 14.1074 11.5071C14.3075 11.3674 14.3887 11.133 14.2672 10.9776L11.0457 6.85827C10.8613 6.62248 10.9655 6.25327 11.2779 6.03523C11.4293 5.92957 11.6062 5.87477 11.7764 5.88085C11.9465 5.88693 12.0895 5.95318 12.1788 6.0674L12.181 6.07025L15.8671 10.6562L15.7576 11.0978C15.4527 11.3918 14.6874 12.2258 14.5502 13.3047C14.5245 13.5074 14.689 13.6551 14.9176 13.6346C15.1462 13.6141 15.3525 13.4332 15.3783 13.2304C15.5058 12.2274 16.3781 11.4707 16.3855 11.4643C16.4638 11.3983 16.5185 11.3144 16.5401 11.2274L17.2682 8.28957C17.3475 7.96948 17.6418 7.68302 18.0006 7.57674C18.2296 7.50885 18.456 7.52045 18.638 7.60933C18.82 7.69819 18.9354 7.85357 18.963 8.04675Z" fill="black"></path>\
                <path d="M19.842 3.30215C20.0513 3.18129 20.1445 2.95077 20.0501 2.78727C19.9557 2.62378 19.7095 2.58923 19.5002 2.7101C19.2908 2.83097 19.1976 3.06149 19.292 3.22498C19.3864 3.38847 19.6326 3.42302 19.842 3.30215Z" fill="black"></path>\
                <path d="M14.2341 5.11155C14.2492 5.10001 15.7715 3.95113 17.8577 3.52672C18.0976 3.47788 18.2876 3.25713 18.2646 3.05513C18.244 2.87405 18.0565 2.76504 17.842 2.80864C15.5149 3.28213 13.8422 4.54435 13.7722 4.59783C13.5806 4.74408 13.5288 4.9776 13.6564 5.11947C13.784 5.26134 14.0426 5.25769 14.2341 5.11155Z" fill="black"></path>\
                <path d="M15.3205 5.2931C15.1184 5.42546 15.0433 5.65761 15.152 5.81233C15.2608 5.96707 15.5132 5.9857 15.7159 5.85382C15.7358 5.841 17.7198 4.57136 19.9704 4.80634C20.201 4.83039 20.455 4.65935 20.5096 4.44422C20.557 4.25715 20.4367 4.09407 20.2365 4.07319C17.6329 3.80134 15.4137 5.23209 15.3205 5.2931Z" fill="black"></path>\
                <path d="M5.53285 14.7613C5.66201 14.5728 5.61311 14.3581 5.42338 14.2814C5.23337 14.2046 4.97403 14.2954 4.84429 14.484C4.80817 14.5365 3.95937 15.7869 3.90517 17.3235C3.89866 17.5078 4.05843 17.6399 4.26837 17.6241C4.50946 17.6059 4.73067 17.4008 4.73814 17.1897C4.78459 15.873 5.52539 14.7723 5.53285 14.7613Z" fill="black"></path>\
                <path d="M5.89352 16.0002C5.87206 16.0523 5.37051 17.2913 5.59341 18.5169C5.62661 18.6995 5.83239 18.7977 6.0518 18.7352C6.28372 18.6691 6.45236 18.4472 6.41726 18.2542C6.22897 17.2189 6.66503 16.1289 6.67124 16.1137C6.75364 15.9126 6.64679 15.7242 6.4323 15.6927C6.21749 15.6613 5.97627 15.7989 5.89352 16.0002Z" fill="black"></path>\
            </svg></span><span class="notification-message-sub-div-1" style="font-family:' + prompt_text_font_family + '"> '+ auto_pop_up_text+'</span></div></div>'
                notification_counter='<div class="allincall-notification-div" onclick="open_up_bot()" style="display:none;" id="allincall-notification-count">1</div>'
                notification_message_div_element = document.createElement("div");
                notification_message_div_element.setAttribute("easyassist_avoid_sync", "true")
                notification_message_div_element.innerHTML += wrapper_html + notification_message_div + '</div></div></div>';            
                notification_counter_element = document.createElement("div");
                notification_counter_element.innerHTML += notification_counter;
                document.body.appendChild( notification_message_div_element)   

                var easychat_popup_image_div = ''
                  if (is_minimization_enabled) 
                {

                    easychat_popup_image_div += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML + easychat_popup_min_image.outerHTML +
                                                          easychat_popup_minimize.outerHTML + easychat_popup_maximize.outerHTML

                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(notification_counter_element)
                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].innerHTML += easychat_popup_image_div

                    document.getElementById("allincall-minimize-popup").appendChild(easychat_popup_minimize_tooltip)
                    document.getElementById("allincall-maximize-popup").appendChild(easychat_popup_maximize_tooltip)
                } else {
                    easychat_popup_image_div += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML

                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(notification_counter_element)
                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].innerHTML += easychat_popup_image_div

                }

            }
            else if(auto_popup_type == "3" && !is_form_assist_auto_pop_allowed){

             popup_enabled = true
             wrapper_html = '<div id="' + id_popup_wrapper + '" class="' + class_popup_wrapper + '">'  
             notification_message_div = '<div class="notification-message-div notification-message-div-intent-bubble" style="display:none;" id="notification-message-div">\
             <div class="intent-bubble-wrapper-div">\
             <div class="notification-message-hide-div notification-message-hide-div-intent-bubble" onclick="hide_auto_pop_up_notification_text()">\
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\
                        <circle cx="12" cy="12" r="11.5" fill="white" stroke="#' + bot_theme_color + '"></circle>\
                        <path d="M16.1839 17L12.5029 13.3156L8.82186 17L8 16.1787L11.6868 12.5L8 8.82134L8.82186 8L12.5029 11.6844L16.1839 8.00578L17 8.82134L13.319 12.5L17 16.1787L16.1839 17Z" fill="#' + bot_theme_color + '"></path>\
                    </svg></div>\
                <div class="notification-message-intent-bubble" onclick="open_up_bot_by_greeting()" style="border: 1px solid #' + bot_theme_color + ';">\
                <span class="notification-message-intent-bubble-sub-text" style="font-family:' + prompt_text_font_family + '">'+ auto_pop_up_text+'</span></div>\
                </div>\
                <div class="notification-intent-message-bubble-container">'
            for(i=0;i<initial_trigger_intents.length;i++){
                notification_message_div+= '<div class="notification-intent-message-bubble" style="background:#' + bot_theme_color + ';font-family:' + prompt_text_font_family + ';" onclick="open_greeting_intents(this, ' + initial_trigger_intents[i][1] + ')">'+initial_trigger_intents[i][0]+'</div>'
            }
                notification_message_div += '</div></div>'
                notification_message_div_element = document.createElement("div");
                notification_message_div_element.setAttribute("easyassist_avoid_sync", "true")
                easychat_popup_image_div = document.createElement('div')
                easychat_popup_image_div.className = class_pop_up_image_wrapper

                if (is_minimization_enabled) {

                    easychat_popup_image_div.innerHTML += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML + easychat_popup_min_image.outerHTML +
                                                           easychat_popup_minimize.outerHTML + easychat_popup_maximize.outerHTML

                     notification_message_div_element.innerHTML += wrapper_html + notification_message_div + '</div>';
                    document.body.appendChild( notification_message_div_element)
                    document.getElementById(id_popup_wrapper).appendChild(easychat_popup_image_div)

                    document.getElementById("allincall-minimize-popup").appendChild(easychat_popup_minimize_tooltip)
                    document.getElementById("allincall-maximize-popup").appendChild(easychat_popup_maximize_tooltip)

                } else {
                    easychat_popup_image_div.innerHTML += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML

                    notification_message_div_element.innerHTML += wrapper_html + notification_message_div + '</div>';
                    document.body.appendChild( notification_message_div_element)
                    document.getElementById(id_popup_wrapper).appendChild(easychat_popup_image_div)
                }
            }
            else if(is_form_assist_auto_pop_allowed && form_assist_intent_bubble_type == "1") {

             popup_enabled = true
             wrapper_html = '<div id="' + id_popup_wrapper + '" class="' + class_popup_wrapper + '"><div class="' + class_pop_up_image_wrapper + '"><div class="' + class_greeting_notification_wrapper + '">'  

             notification_message_div = '<div class="notification-message-div" style="display:none;" id="notification-message-div">\
                <div class="notification-message-hide-div" onclick="hide_auto_pop_up_notification_text()">\
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\
                        <circle cx="12" cy="12" r="11.5" fill="white" stroke="#' + bot_theme_color + '"></circle>\
                        <path d="M16.1839 17L12.5029 13.3156L8.82186 17L8 16.1787L11.6868 12.5L8 8.82134L8.82186 8L12.5029 11.6844L16.1839 8.00578L17 8.82134L13.319 12.5L17 16.1787L16.1839 17Z" fill="#' + bot_theme_color + '"></path>\
                    </svg></div>\
                <div class="allincall-notification-message" onclick="open_up_bot_by_greeting()" style="border: 1px solid #' + bot_theme_color + ';">\
                <span> <svg width="28" height="26" viewBox="0 0 28 26" fill="none" xmlns="http://www.w3.org/2000/svg">\
                <path d="M10.8896 17.2108L6.68998 11.8405C6.68998 11.8405 5.86993 10.2885 8.0351 10.1679C8.0351 10.1679 7.07822 8.44705 9.41351 7.95764C9.41351 7.95764 8.39557 6.90729 9.47268 6.15549C10.5498 5.40368 11.3032 6.66714 11.3032 6.66714C11.3032 6.66714 12.6303 4.65722 13.7123 6.04074C14.7942 7.42426 17.3097 10.5104 17.3097 10.5104C17.3097 10.5104 17.5153 7.53379 18.9477 7.22838C20.0809 6.98676 20.3276 7.73942 20.3276 7.73942C20.3276 7.73942 20.6095 10.3757 20.8806 11.4605C21.2576 12.9685 21.2556 14.5389 20.7254 15.5043L22.647 17.9617L16.7544 21.3638L15.0816 19.0005C15.0818 19.0005 12.7019 19.5282 10.8896 17.2108Z" fill="#FFD3B4"></path>\
                <path d="M17.8963 6.8808C17.1904 7.08995 16.6113 7.65362 16.4551 8.28353L16.1311 9.59087L12.8952 5.56503C12.6927 5.30703 12.3692 5.1574 11.9843 5.14364C11.5986 5.12984 11.1972 5.2541 10.8542 5.49353C10.6405 5.64271 10.4701 5.82326 10.3474 6.01718C9.8672 5.46932 8.94834 5.4056 8.26151 5.88506C7.90833 6.1316 7.67143 6.47887 7.59459 6.86288C7.52658 7.20259 7.59313 7.53503 7.78187 7.80679C7.54522 7.86184 7.31348 7.96496 7.10368 8.11143C6.76065 8.35084 6.51703 8.67677 6.41767 9.02913C6.3389 9.30844 6.35864 9.57767 6.47085 9.80635C6.22741 9.8605 5.98852 9.96566 5.77264 10.1163C5.43019 10.3553 5.18626 10.6803 5.08584 11.0312C4.98511 11.3833 5.0407 11.7191 5.24235 11.977L9.81505 17.8243C10.6978 18.9532 12.1727 19.5466 13.8853 19.4695L15.3883 21.6038C15.492 21.751 15.727 21.7759 15.9264 21.6608L21.819 18.2587C21.927 18.1964 22.0091 18.1011 22.0449 17.9967C22.0807 17.8923 22.0667 17.7886 22.0065 17.7116L20.1866 15.3844C20.4727 14.6697 21.1083 12.9046 20.2883 11.2934L19.7904 7.80573C19.7361 7.42552 19.5089 7.11981 19.1507 6.9449C18.7926 6.76999 18.3471 6.74725 17.8963 6.8808ZM18.963 8.04675L19.4676 11.5814C19.4722 11.6132 19.4818 11.6433 19.4964 11.6709C20.2728 13.1475 19.5867 14.8345 19.3612 15.3889L19.3361 15.4508C19.2916 15.5612 19.3031 15.6733 19.3673 15.7552L21.0525 17.9103L15.9379 20.8632L14.5197 18.8493C14.456 18.7587 14.339 18.7111 14.2056 18.7214C12.659 18.8402 11.3203 18.3307 10.5326 17.3235L5.95993 11.4762C5.87205 11.3638 5.8479 11.217 5.89201 11.0629C5.93639 10.9078 6.04444 10.764 6.19621 10.6581C6.34818 10.5521 6.52523 10.4968 6.69515 10.5023C6.86398 10.5078 7.00542 10.5727 7.0933 10.685L9.74996 14.0822C9.87267 14.2391 10.1677 14.2621 10.3765 14.1118C10.5672 13.9745 10.6303 13.741 10.5165 13.5955L7.29516 9.47616C7.20586 9.36194 7.18078 9.21345 7.2246 9.05797C7.26844 8.90253 7.37592 8.75874 7.52727 8.65312C7.67849 8.54754 7.85561 8.49268 8.02576 8.49876C8.19591 8.50485 8.33883 8.57109 8.42813 8.68531L11.6495 12.8047C11.7713 12.9604 12.0325 12.9554 12.2327 12.8155C12.4324 12.676 12.513 12.4416 12.3918 12.2865L8.54056 7.36173C8.42201 7.21013 8.37731 7.02382 8.41469 6.83706C8.44799 6.67097 8.54398 6.52524 8.68514 6.42673C8.99728 6.20882 9.4409 6.27335 9.67364 6.5709L13.5249 11.4957C13.6464 11.651 13.9075 11.6466 14.1074 11.5071C14.3075 11.3674 14.3887 11.133 14.2672 10.9776L11.0457 6.85827C10.8613 6.62248 10.9655 6.25327 11.2779 6.03523C11.4293 5.92957 11.6062 5.87477 11.7764 5.88085C11.9465 5.88693 12.0895 5.95318 12.1788 6.0674L12.181 6.07025L15.8671 10.6562L15.7576 11.0978C15.4527 11.3918 14.6874 12.2258 14.5502 13.3047C14.5245 13.5074 14.689 13.6551 14.9176 13.6346C15.1462 13.6141 15.3525 13.4332 15.3783 13.2304C15.5058 12.2274 16.3781 11.4707 16.3855 11.4643C16.4638 11.3983 16.5185 11.3144 16.5401 11.2274L17.2682 8.28957C17.3475 7.96948 17.6418 7.68302 18.0006 7.57674C18.2296 7.50885 18.456 7.52045 18.638 7.60933C18.82 7.69819 18.9354 7.85357 18.963 8.04675Z" fill="black"></path>\
                <path d="M19.842 3.30215C20.0513 3.18129 20.1445 2.95077 20.0501 2.78727C19.9557 2.62378 19.7095 2.58923 19.5002 2.7101C19.2908 2.83097 19.1976 3.06149 19.292 3.22498C19.3864 3.38847 19.6326 3.42302 19.842 3.30215Z" fill="black"></path>\
                <path d="M14.2341 5.11155C14.2492 5.10001 15.7715 3.95113 17.8577 3.52672C18.0976 3.47788 18.2876 3.25713 18.2646 3.05513C18.244 2.87405 18.0565 2.76504 17.842 2.80864C15.5149 3.28213 13.8422 4.54435 13.7722 4.59783C13.5806 4.74408 13.5288 4.9776 13.6564 5.11947C13.784 5.26134 14.0426 5.25769 14.2341 5.11155Z" fill="black"></path>\
                <path d="M15.3205 5.2931C15.1184 5.42546 15.0433 5.65761 15.152 5.81233C15.2608 5.96707 15.5132 5.9857 15.7159 5.85382C15.7358 5.841 17.7198 4.57136 19.9704 4.80634C20.201 4.83039 20.455 4.65935 20.5096 4.44422C20.557 4.25715 20.4367 4.09407 20.2365 4.07319C17.6329 3.80134 15.4137 5.23209 15.3205 5.2931Z" fill="black"></path>\
                <path d="M5.53285 14.7613C5.66201 14.5728 5.61311 14.3581 5.42338 14.2814C5.23337 14.2046 4.97403 14.2954 4.84429 14.484C4.80817 14.5365 3.95937 15.7869 3.90517 17.3235C3.89866 17.5078 4.05843 17.6399 4.26837 17.6241C4.50946 17.6059 4.73067 17.4008 4.73814 17.1897C4.78459 15.873 5.52539 14.7723 5.53285 14.7613Z" fill="black"></path>\
                <path d="M5.89352 16.0002C5.87206 16.0523 5.37051 17.2913 5.59341 18.5169C5.62661 18.6995 5.83239 18.7977 6.0518 18.7352C6.28372 18.6691 6.45236 18.4472 6.41726 18.2542C6.22897 17.2189 6.66503 16.1289 6.67124 16.1137C6.75364 15.9126 6.64679 15.7242 6.4323 15.6927C6.21749 15.6613 5.97627 15.7989 5.89352 16.0002Z" fill="black"></path>\
            </svg></span><span class="notification-message-sub-div-1" id="form-assist-pop-up-text-for-type-1" style="font-family:' + prompt_text_font_family + '"> '+ form_assist_auto_pop_text +'</span></div></div>'
                notification_counter='<div class="allincall-notification-div" onclick="open_up_bot()" style="display:none;" id="allincall-notification-count">1</div>'
                notification_message_div_element = document.createElement("div");
                notification_message_div_element.setAttribute("easyassist_avoid_sync", "true")
                notification_message_div_element.innerHTML += wrapper_html + notification_message_div + '</div></div></div>';            
                notification_counter_element = document.createElement("div");
                notification_counter_element.innerHTML += notification_counter;
                document.body.appendChild( notification_message_div_element)  

                 var easychat_popup_image_div = ''
                  if (is_minimization_enabled) 
                {

                    easychat_popup_image_div += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML + easychat_popup_min_image.outerHTML +
                                                          easychat_popup_minimize.outerHTML + easychat_popup_maximize.outerHTML

                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(notification_counter_element)
                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].innerHTML += easychat_popup_image_div

                    document.getElementById("allincall-minimize-popup").appendChild(easychat_popup_minimize_tooltip)
                    document.getElementById("allincall-maximize-popup").appendChild(easychat_popup_maximize_tooltip)
                } else {
                    easychat_popup_image_div += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML

                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(notification_counter_element)
                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].innerHTML += easychat_popup_image_div

                }      
            }
            else if(is_form_assist_auto_pop_allowed && form_assist_intent_bubble_type == "2") {

             popup_enabled = true
             wrapper_html = '<div id="' + id_popup_wrapper + '" class="' + class_popup_wrapper + '">'  
             notification_message_div = '<div class="notification-message-div notification-message-div-intent-bubble" style="display:none;" id="notification-message-div">\
                <div class="notification-message-hide-div notification-message-hide-div-intent-bubble" onclick="hide_auto_pop_up_notification_text()">\
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\
                        <circle cx="12" cy="12" r="11.5" fill="white" stroke="#' + bot_theme_color + '"></circle>\
                        <path d="M16.1839 17L12.5029 13.3156L8.82186 17L8 16.1787L11.6868 12.5L8 8.82134L8.82186 8L12.5029 11.6844L16.1839 8.00578L17 8.82134L13.319 12.5L17 16.1787L16.1839 17Z" fill="#' + bot_theme_color + '"></path>\
                    </svg></div>\
                <div class="notification-message-intent-bubble" id="intent-bubble-greeting-message" onclick="open_up_bot_by_greeting()" style="border: 1px solid #' + bot_theme_color + ';">\
                <span class="notification-message-intent-bubble-sub-text" style="font-family:' + prompt_text_font_family + '">'+ form_assist_auto_pop_text +'</span></div>\
                <div style="direction: rtl;">'
            for (var intent_pk in form_assist_intent_bubble) {
                notification_message_div+= '<div class="notification-intent-message-bubble form-assist-intent-bubble" id="' + intent_pk + '" style="border-radius:4px;background:#' + bot_theme_color + ';font-size: 14px;padding: 4px 14px 5px 14px;margin-bottom:4px;color: #FFF;text-align: center;line-height: 25px;width:max-content;transform-origin: 100% 0;transition: 0.3s ease;font-weight: 600;font-family:' + prompt_text_font_family + ';direction: ltr;" onclick="open_form_assist_greeting_intent(this)">' + form_assist_intent_bubble[intent_pk] + '</div>'
            }
            for (var intent_pk in form_assist_tag_intents){
                if(intent_pk in form_assist_intent_bubble) continue;
                notification_message_div+= '<div class="notification-intent-message-bubble form-assist-intent-bubble" id="' + intent_pk + '" style="border-radius:4px;background:#' + bot_theme_color + ';font-size: 14px;padding: 4px 14px 5px 14px;margin-bottom:4px;color: #FFF;text-align: center;line-height: 25px;width:max-content;transform-origin: 100% 0;transition: 0.3s ease;font-weight: 600;font-family:' + prompt_text_font_family + ';direction: ltr;" onclick="open_form_assist_greeting_intent(this)">' + form_assist_tag_intents[intent_pk] + '</div>'
            }
                notification_message_div += '</div></div>'
                notification_message_div_element = document.createElement("div");
                notification_message_div_element.setAttribute("easyassist_avoid_sync", "true")
                easychat_popup_image_div = document.createElement('div')
                easychat_popup_image_div.className = class_pop_up_image_wrapper

                if (is_minimization_enabled) 
            {

                easychat_popup_image_div.innerHTML += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML + easychat_popup_min_image.outerHTML +
                                                       easychat_popup_minimize.outerHTML + easychat_popup_maximize.outerHTML

                 notification_message_div_element.innerHTML += wrapper_html + notification_message_div + '</div>';
                document.body.appendChild( notification_message_div_element)
                document.getElementById(id_popup_wrapper).appendChild(easychat_popup_image_div)

                    document.getElementById("allincall-minimize-popup").appendChild(easychat_popup_minimize_tooltip)
                    document.getElementById("allincall-maximize-popup").appendChild(easychat_popup_maximize_tooltip)

            } else {
                easychat_popup_image_div.innerHTML += easychat_popup_image.outerHTML + easychat_popup_close_button.outerHTML

                notification_message_div_element.innerHTML += wrapper_html + notification_message_div + '</div>';
                document.body.appendChild( notification_message_div_element)
                document.getElementById(id_popup_wrapper).appendChild(easychat_popup_image_div)
            }              

            } 
                
            notification_counter='<div class="new-notification-div" style="display:none;" onclick="open_up_bot()" id="new-notification-div">\
                                    <svg width="53" height="53" viewBox="0 0 53 53" fill="none" xmlns="http://www.w3.org/2000/svg">\
                                    <path d="M6.23139 48.0527C7.33445 46.1811 8.68728 43.7736 9.91886 41.4867L10.0507 41.2415L9.83274 41.0693C4.78184 37.079 2 31.6803 2 25.8689C2 14.3619 13.1446 5.00013 26.8438 5.00013C40.5429 5.00013 51.6875 14.3619 51.6875 25.8689C51.6875 37.3758 40.5429 46.7376 26.8438 46.7376C23.8691 46.7376 20.9568 46.2984 18.1862 45.4332L18.0782 45.3994L17.9722 45.4391C13.7965 46.9861 9.46571 47.946 6.23139 48.0527Z" fill="#'+bot_theme_color+'"></path>\
                                    <text id="new-notification-count" x="22" y="30" font-family="Silka" font-size="15px" font-weight="700" fill="#fff">1</text>\
                                    </svg>\
                                    </div>'  

            notification_counter_element = document.createElement("div");
            notification_counter_element.innerHTML += notification_counter;

            // This is to colour the notification pseudo element to theme color
            const root = document.querySelector(":root");
            root.style.setProperty("--pseudo-bordercolor", "#" + bot_theme_color);

            if (is_form_assist == "true") {
                callFormAssist()
            }

            show_web_landing_intents(bot_theme_color, BOT_POSITION, easychat_popup_min_image);

            if (popup_enabled == false)
            {
                wrapper_html = '<div id="' + id_popup_wrapper + '" class="' + class_popup_wrapper + '"><div class="' + class_pop_up_image_wrapper + '">'  
                notification_message_div_element = document.createElement("div");
                notification_message_div_element.setAttribute("easyassist_avoid_sync", "true")
                notification_message_div_element.innerHTML += wrapper_html + '</div></div>';  
                document.body.appendChild(notification_message_div_element)              
                document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(easychat_popup_image);
                document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(easychat_popup_close_button);
            }

            document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(notification_counter_element)
            change_css_on_bot_maximization(BOT_POSITION)

            if (is_minimization_enabled) {
                if (popup_enabled == false) {
                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(easychat_popup_min_image);
                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(easychat_popup_minimize);
                    document.getElementById("allincall-minimize-popup").appendChild(easychat_popup_minimize_tooltip);
                    document.getElementsByClassName(class_pop_up_image_wrapper)[0].appendChild(easychat_popup_maximize);
                    document.getElementById("allincall-maximize-popup").appendChild(easychat_popup_maximize_tooltip);
                }

                document.getElementById("allincall-minimize-popup").addEventListener("click", function(e) {
                    document.getElementById("allincall-popup").style.display = "none";
                    document.getElementById("allincall-min-popup").style.display = "block";
                    document.getElementById("allincall-maximize-popup").style.display = "flex";
                    document.getElementById("allincall-minimize-popup").style.display = "none";
                    document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
                    document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";

                    change_css_on_bot_minimization(BOT_POSITION);   
                    if(window.disable_auto_popup_minimized){
                        let date = new Date();
                        date.setTime(date.getTime()+(24*60*60*1000));
                        easychat_set_cookie('is_bot_minimized', 'true', date.toGMTString(), "")
                        if(document.getElementById("allincall-notification-count")){
                            document.getElementById("allincall-notification-count").style.display = "none";
                        }
                        document.getElementById("notification-message-div").style.display = "none";
                    }                 
                     
                });

                document.getElementById("allincall-minimize-popup").addEventListener("mouseover", function(e) {
                    document.getElementById("allincall-minimize-popup").style.backgroundColor = "#" + bot_theme_color;
                    document.getElementById("allincall-minimize-popup-tooltip").textContent = MINIMIZE_TEXT;
                    document.getElementById("allincall-minimize-popup-tooltip").style.fontFamily = prompt_text_font_family;
                    document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "unset";
                });

                document.getElementById("allincall-minimize-popup").addEventListener("mouseout", function(e) {
                    document.getElementById("allincall-minimize-popup").style.backgroundColor = "";
                    document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";
                    document.getElementById("allincall-minimize-popup").style.fontColor = "black";

                });

                document.getElementById("allincall-maximize-popup").addEventListener("click", function(e) {
                    document.getElementById("allincall-popup").style.display = "block";
                    document.getElementById("allincall-min-popup").style.display = "none";
                    document.getElementById("allincall-maximize-popup").style.display = "none";
                    document.getElementById("allincall-minimize-popup").style.display = "flex";
                    document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
                    document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";

                    change_css_on_bot_maximization(BOT_POSITION)   
                    if(window.disable_auto_popup_minimized){
                        let date = new Date();
                        date.setTime(date.getTime()+(24*60*60*1000));
                        easychat_set_cookie('is_bot_minimized', 'false', date.toGMTString(), "");
                        check_auto_popup();
                        check_campaign_link();
                        show_web_landing_intents(bot_theme_color, BOT_POSITION, easychat_popup_min_image);
                        if (is_form_assist == "true") {
                            element_id = ''
                            resetTimer(e, true)
                        }
                    }                  
                    
                });

                document.getElementById("allincall-maximize-popup").addEventListener("mouseover", function(e) {
                    document.getElementById("allincall-maximize-popup").style.backgroundColor = "#" + bot_theme_color;
                    document.getElementById("allincall-maximize-popup-tooltip").textContent = MAXIMIZE_TEXT;
                    document.getElementById("allincall-maximize-popup-tooltip").style.fontFamily = prompt_text_font_family;
                    document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "unset";
                });

                document.getElementById("allincall-maximize-popup").addEventListener("mouseout", function(e) {
                    document.getElementById("allincall-maximize-popup").style.backgroundColor = "";
                    document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
                    document.getElementById("allincall-maximize-popup").style.fontColor = "black";

                });
                check_and_change_state_of_bot();
            }

            document.getElementById("easychat-bot-close-button").addEventListener("click", function(e) {
                is_initial_trigger_intent = false;
                trigger_intent_pk = "";
                easychat_intent_name = "";
                document.getElementById("allincall-chat-box").contentWindow.postMessage({
                                event_id: 'close-chatbot',
                                data: is_nps_required,
                                data: is_nps_required,
                            }, "*")
                setTimeout(function() {
                    if(window.disable_auto_popup_minimized  && get_cookie('is_bot_minimized') == 'true'){
                        document.getElementById("allincall-popup").style.display = "none";
                        document.getElementById("allincall-min-popup").style.display = "block";
                        document.getElementById("allincall-maximize-popup").style.display = "flex";
                        document.getElementById("allincall-minimize-popup").style.display = "none";
                        document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
                        document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";
                            
                        change_css_on_bot_minimization(BOT_POSITION)
                    }
                }, 1030)
            });
            [document.getElementById("allincall-popup"), document.getElementById("allincall-min-popup")].forEach(function(element) {
                if (element == null) {
                    return;
                }
                element.addEventListener("click", function(e) {
                    set_auto_popup_not_required_cookie();
                    if (auto_popup != null) {
                        clearTimeout(auto_popup)
                    }

                    if(easychat_minimized_chatbot == false){
                        save_bot_click_count();
                    }
                    
                    document.getElementById("allincall-chat-box").contentWindow.postMessage({
                        event_id: 'is_chatbot_opened',
                        data: true,
                    }, "*")

                    if(document.getElementById("notification-message-div") !=null  && document.getElementById("notification-message-div")!= undefined ){
                        document.getElementById("notification-message-div").style.display ="none"
                         
                    }
                    
                    if(document.getElementById("allincall-notification-count") !=null  && document.getElementById("allincall-notification-count")!= undefined ){
                        
                         document.getElementById("allincall-notification-count").style.display ="none"
                    }

                    if(document.getElementById("new-notification-div") !=null  && document.getElementById("new-notification-div")!= undefined ){ 
                        document.getElementById("new-notification-div").style.display ="none"
                    }
                    try {
                        website_cookies = getCookies()
                        website_cookies = JSON.stringify(website_cookies)
                        website_cookies = encrypt_variable(website_cookies)
                        chat_bot_maximized = true
                        try {
                            document.getElementById("one-popup-on-bot").style.display = "none";
                            document.getElementById("chatbox-notification").style.display = "none";
                            document.getElementById("allincall-popup").style.zIndex = "99999999";
                            document.getElementById("cross-chatbox-notification").remove();

                        } catch (err) {}

                    } catch (err) { console.log(err) }

                    document.getElementById("allincall-chat-box").style.display = "block";
                    document.getElementById("easychat-bot-close-button").style.display = "block";
                    
                    if (is_minimization_enabled) {
                        document.getElementById("allincall-minimize-popup").style.display = "none";
                        document.getElementById("allincall-maximize-popup").style.display = "none";
                        document.getElementById("allincall-min-popup").style.display = "none";
                    }
                    if (is_form_assist == 'true') {
                        easychat_do_not_disturb = is_form_assist_active()
                        if(window.form_assist_auto_popup_type == "1" || (window.form_assist_auto_popup_type == "2" && easychat_intent_name != "" && is_initial_trigger_intent)) {
                            easychat_form_assist_id = get_form_assist_id();
                        }
                        if(easychat_form_assist_id != "" && window.voice_based_form_assist_enabled) {
                            is_voice_based_form_assist_enabled = true;
                        }
                        console.log("Do not Disturb: " + easychat_do_not_disturb)
                        if (easychat_do_not_disturb == true && easychat_form_assist_id == "") {
                            is_trigger_bot_allowed = 0;
                            openChatBot();
                        } else if (easychat_form_assist_id != "" || easychat_minimized_chatbot == false) {
                            
                            document.getElementById("allincall-chat-box").src = SERVER_URL + "/chat/index/?id=" + BOT_ID + '&name=' + BOT_NAME + '&theme=' + BOT_THEME + '&easychat_window_location=' + easychat_window_location + '&form_assist_id=' + easychat_form_assist_id + '&do_not_disturb=' + easychat_do_not_disturb + '&is_lead_generation=' + is_lead_generation + '&lead_generation_intent_id=' + lead_generation_intent_id + '&page_category=' + easychat_page_category.toString() + '&meta_data=' + meta_tags_information + '&is_web_landing_allowed=' + is_web_landing_allowed + '&campaign_link_query_id=' + campaign_link_query_id + '&selected_language=' + selected_language + '&is_initial_trigger_intent=' + is_initial_trigger_intent + '&web_page_source=' + web_page_source + "&query_question=" + welcome_banner_query_question + "&external_trigger_info=" + external_trigger_intent_info + "&is_voice_based_form_assist_enabled=" + is_voice_based_form_assist_enabled + "&enable_response_form_assist=" + enable_response_form_assist + "&trigger_intent_pk=" + trigger_intent_pk + "&easychat_intent_name=" + easychat_intent_name.replace("&", "%26") + "&is_geolocation_enabled=" + is_geolocation_enabled;
                            welcome_banner_query_question = "INTENT_NAME";
                            external_trigger_intent_info = "INTENT_INFO";
                            trigger_intent_pk = "";
                            easychat_intent_name = "";
                            is_initial_trigger_intent = false;
                            is_web_landing_allowed = false;

                            // document.getElementById("allincall-chat-box").contentWindow.postMessage('open-chatbot','*')
                            //document.getElementById("chatbox-notification").style.display = "none"
                            try {
                                document.getElementById("one-popup-on-bot").style.display = "none";
                                document.getElementById("chatbox-notification").style.display = "none";
                                document.getElementById("allincall-popup").style.zIndex = "99999999";
                                document.getElementById("cross-chatbox-notification").style.display = "none";
                            } catch (err) {}


                        }
                    } else if (easychat_minimized_chatbot != true) {
                        document.getElementById("allincall-chat-box").src = SERVER_URL + "/chat/index/?id=" + BOT_ID + '&name=' + BOT_NAME + '&theme=' + BOT_THEME + '&easychat_window_location=' + easychat_window_location + '&form_assist_id=' + easychat_form_assist_id + '&do_not_disturb=' + easychat_do_not_disturb + '&is_lead_generation=' + is_lead_generation + '&lead_generation_intent_id=' + lead_generation_intent_id + '&page_category=' + easychat_page_category.toString() + '&meta_data=' + meta_tags_information + '&is_web_landing_allowed=' + is_web_landing_allowed + '&campaign_link_query_id=' + campaign_link_query_id + '&selected_language=' + selected_language + '&is_initial_trigger_intent=' + is_initial_trigger_intent + '&web_page_source=' + web_page_source+ "&query_question=" + welcome_banner_query_question + "&external_trigger_info=" + external_trigger_intent_info + "&is_voice_based_form_assist_enabled=" + is_voice_based_form_assist_enabled + "&trigger_intent_pk=" + trigger_intent_pk + "&easychat_intent_name=" + easychat_intent_name.replace("&", "%26") + "&is_geolocation_enabled=" + is_geolocation_enabled;
                        welcome_banner_query_question = "INTENT_NAME";
                        external_trigger_intent_info = "INTENT_INFO";
                        trigger_intent_pk = "";
                        easychat_intent_name = "";
                        is_web_landing_allowed = false;

                        // document.getElementById("allincall-chat-box").contentWindow.postMessage('open-chatbot','*')
                        if (!get_cookie("isFeedBackDone")) {
                            easychat_set_cookie("isFeedBackDone", "0", "", "")
                        }
                        try {
                            document.getElementById("chatbox-notification").style.display = "none";
                            document.getElementById("allincall-popup").style.zIndex = "99999999";
                            document.getElementById("cross-chatbox-notification").style.display = "none";
                            document.getElementById("one-popup-on-bot").style.display = "none";
                            setTimeout(function(e) {
                                document.getElementById("allincall-chat-box").contentWindow.postMessage({
                                    event_id: 'isFeedBackDone',
                                    data: get_cookie("isFeedBackDone")
                                }, "*")
                            }, 2000);
                        } catch (err) {}


                        // set livechat cookie
                        if (!get_cookie("livechat_cookie_session_id")) {
                            easychat_set_cookie("livechat_cookie_session_id", "", "", "/")
                        }
                        setTimeout(function(e) {
                            document.getElementById("allincall-chat-box").contentWindow.postMessage({
                                event_id: 'livechat_cookie_session_user_id',
                                livechat_cookie_session_id: get_cookie("livechat_cookie_session_id"),
                            }, "*")
                        }, 1000);
                    }

                    this.style.display = "none";
                    document.body.style.overflow = "unset";
                    var chat_box_window = document.getElementById("allincall-chat-box");

                    if ((window.innerWidth < 500)) {
                        chat_box_window.style.display = "block";
                        chat_box_window.style.height = "100%";
                        chat_box_window.style.bottom = "0em";
                        chat_box_window.style.right = "0em";
                        //chat_box_window.style.animationName = "my-amine-blo";
                        try {
                            chat_box_window.classList.remove("animate__animated")
                            chat_box_window.classList.remove("animate__slideOutDown")
                            chat_box_window.classList.remove("allincall-scale-out-br")
                        } catch (err) {}
                        chat_box_window.className += "animate__animated animate__slideInUp";
                    } else {

                        if (BOT_POSITION == "right") {
                            chat_box_window.style.display = "block";
                            chat_box_window.style.right = "1em";
                            chat_box_window.style.animationName = "right-anime";
                        }
                        if (BOT_POSITION == "left") {
                            chat_box_window.style.display = "block";
                            chat_box_window.style.left = "1em"
                            chat_box_window.style.animationName = "left-anime";
                        }
                        if (BOT_POSITION == "bottom-right") {
                            try {
                                chat_box_window.classList.remove("animate__animated")
                                chat_box_window.classList.remove("animate__slideOutDown")
                                chat_box_window.classList.remove("allincall-scale-out-br")
                            } catch (err) {}
                            chat_box_window.className += "animate__animated animate__slideInUp";
                            chat_box_window.style.display = "block";
                            chat_box_window.style.bottom = "1em";
                            chat_box_window.style.right = "2em";
                            //chat_box_window.style.animationName = "bottom-left-right-anime";
                        }
                        if (BOT_POSITION == "top-right") {
                            chat_box_window.style.display = "block";
                            chat_box_window.style.right = "1em";
                            chat_box_window.style.top = "1em";
                            chat_box_window.style.animationName = "right-anime";
                        }
                        if (BOT_POSITION == "bottom-left") {
                            try {
                                chat_box_window.classList.remove("animate__animated")
                                chat_box_window.classList.remove("animate__slideOutDown")
                                chat_box_window.classList.remove("allincall-scale-out-bl")
                            } catch (err) {}
                            chat_box_window.className += "animate__animated animate__slideInUp";
                            chat_box_window.style.display = "block";
                            chat_box_window.style.left = "1em";
                            chat_box_window.style.bottom = "1em";
                            //chat_box_window.style.animationName = "bottom-left-right-anime";

                        }
                        if (BOT_POSITION == "top-left") {
                            chat_box_window.style.display = "block";
                            chat_box_window.style.left = "1em";
                            chat_box_window.style.top = "1em";
                            chat_box_window.style.animationName = "left-anime";
                        }
                    }
                });
            });
            if (is_lead_generation == 'true') {
                setTimeout(function(e) {
                    document.getElementById("allincall-popup").click();
                }, 3000)
            }
            
            check_auto_popup();
            check_campaign_link();
            check_welcome_banner_question();
        }
    }
    xhttp.send(params);

    window.addEventListener('message', function(event) {
        // IMPORTANT: Check the origin of the data! 
        if (~event.origin.indexOf(SERVER_URL)) {

            // The data has been sent from your site 
            // The data sent with postMessage is stored in event.data
            
            // Setting selected_language in local storage
            if (event.data.event_id === "set_local_storage") {
                window.localStorage["selected_language"] = event.data.data.var_value
                selected_language = event.data.data.var_value;
            }
            // setting cookie if user stopped autopop-up

            if (event.data.event_id === "auto_pop_up_denied") {

                easychat_set_cookie(event.data.data.cookie_name, event.data.data.cookie_value, event.data.data.expiration, event.data.data.path);
            }
            
            // setting feedback done cookie
            if (event.data.event_id === "isFeedBackDone") {
                easychat_set_cookie("isFeedBackDone", event.data.data, "", "")
            }

            // setting livechat session cookie and user id cookie
            if (event.data.event_id === "livechat_cookie_session_user_id") {
                easychat_set_cookie("livechat_cookie_session_id", event.data.data.livechat_cookie_session_id, "", "/")
            }

            if (event.data.event_id === "unset_livechat_cookies") {
                easychat_set_cookie("livechat_cookie_session_id", "", new Date().getTime(), "/")
            }

            if (event.data.event_id === "create-cobrowsing-lead" && is_easyassist_enabled == "true") {
                create_easyassist_cobrowsing_lead(event.data.data.phone, "Mobile Number");
                if (is_form_assist == "true") {
                    stop_all_activity();
                    window.clearTimeout(timer);
                }
                // $('#allincall-chat-box', window.document).hide("slow");
                // $('#allincall-popup', window.document).show("slow");
                //console.log("cobrowsing has been initiated");
                return;
            }

            if (event.data.event_id === "connect-with-agent" && is_easyassist_enabled == "true") {
                connect_with_easyassist_agent_with_details(event.data.data.full_name, event.data.data.mobile_number);
                if (is_form_assist == "true") {
                    stop_all_activity();
                    window.clearTimeout(timer);
                }
                //$('#allincall-chat-box', window.document).hide("slow");
                //$('#allincall-popup', window.document).show("slow");
                document.getElementById('allincall-chat-box').style.display="none";
                document.getElementById("easychat-bot-close-button").style.display = "none";
                document.getElementById('allincall-popup').style.display = 'block';
                // document.getElementById("allincall-minimize-popup").style.display = "block";
                return;
            }

            if (event.data.event_id === 'initialize-cobrowse') {
                connect_with_cobrowse_agent(event.data.data.username, event.data.data.phone, event.data.data.livechat_session_id, event.data.data.cobrowsing_meeting_id, event.data.data.assigned_agent_username)
            }

            if (event.data.event_id === "set_cookie") {
                easychat_set_cookie(event.data.data.cookie_name, event.data.data.cookie_value, event.data.data.expiration, event.data.data.path);
                return;
            }

            if (event.data.event_id === "send_livechat_session_id") {
                document.getElementById("allincall-chat-box").contentWindow.postMessage({
                    event_id: 'livechat_cookie_session_user_id',
                    livechat_cookie_session_id: get_cookie("livechat_cookie_session_id"),
                }, "*")
            }

            if (is_form_assist == 'true') {
                if (event.data == "disable-form-assist") {
                    close_chatbot_animation()
                    setTimeout(function() {
                        document.getElementById("allincall-popup").style.display = "block";
                        if (is_minimization_enabled) {
                            document.getElementById("allincall-minimize-popup").style.display = "flex";
                            if (window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') == 'true'){
                                document.getElementById("allincall-popup").style.display = "none";
                                document.getElementById("allincall-min-popup").style.display = "block";
                                document.getElementById("allincall-maximize-popup").style.display = "flex";
                                document.getElementById("allincall-minimize-popup").style.display = "none";
                                document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
                                document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";
                                change_css_on_bot_minimization(BOT_POSITION)
                            }
                        }
                        document.getElementById("allincall-chat-box").style.display = "none";
                        document.getElementById("easychat-bot-close-button").style.display = "none"
                    }, 1000);
                    easychat_form_assist_id = "";
                    element_id = ""
                    window.clearTimeout(timer);
                    stop_all_activity()
                }
                if (event.data == "enable-form-assist") {
                    window.clearTimeout(timer);
                    enable_form_assist()
                }
            }

            if (event.data.event_id == "minimize-chatbot") {
                is_bot_minimized = true
                document.getElementById("allincall-chat-box").contentWindow.postMessage({
                    event_id: 'chatbot_minimized_state',
                    data: is_bot_minimized

                }, "*")
                minimize_chatbot_animation();

                MINIMIZE_TEXT = event.data.data.minimize_text;
                MAXIMIZE_TEXT = event.data.data.maximize_text;
                
                setTimeout(function() {
                    document.getElementById("allincall-popup").style.display = "block";
                    if (is_minimization_enabled) {
                        document.getElementById("allincall-minimize-popup").style.display = "flex";
                        if (window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') == 'true'){
                            document.getElementById("allincall-popup").style.display = "none";
                            document.getElementById("allincall-min-popup").style.display = "block";
                            document.getElementById("allincall-maximize-popup").style.display = "flex";
                            document.getElementById("allincall-minimize-popup").style.display = "none";
                            document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
                            document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";
                            change_css_on_bot_minimization(BOT_POSITION)
                        }
                    }
                    document.getElementById("allincall-chat-box").style.display = "none";
                    document.getElementById("easychat-bot-close-button").style.display = "none";
                    
                }, 1000);
                easychat_minimized_chatbot = true;
                easychat_page_category = "";
                easychat_form_assist_id = "";
                if (is_form_assist == 'true') {
                    element_id = ""
                    window.starting_element = false
                    window.clearTimeout(auto_form_pop_timer)
                    window.clearTimeout(timer);
                    timer_is_on = 0
                    check_user_activity_status()
                }
            }
           
           
            if (event.data.event_id == "agent_unread_message"){
                document.getElementById("new-notification-count").innerHTML=event.data.data["message_count"];
                document.getElementById("new-notification-div").style.display="flex";

            }
            if (event.data.event_id == "chatbot_minimized_state") {
                document.getElementById("allincall-popup").click();
                document.getElementById("allincall-notification-count").style.display="none";
                is_bot_minimized = false
                    // document.getElementById('tooltiptext-minimize').style.display ="block";
                document.getElementById("allincall-chat-box").contentWindow.postMessage({
                    event_id: 'chatbot_minimized_state',
                    data: is_bot_minimized
                }, "*")
                // document.getElementById("allincall-chat-box").contentWindow.postMessage({
                //     event_id: 'agent_unread_message',
                //     data: 0
                // }, "*")

            }
            // if(event.data.event_id == "easychat_bot_unread_message"){
            //     document.getElementById("notification-count").innerHTML=event.data.data;
            //     document.getElementById("notification-count").style.display="flex"
            // }
            if (event.data == "close-bot") {
                close_chatbot_animation()
                setTimeout(function() {
                    document.getElementById("allincall-popup").style.display = "block";
                    if (is_minimization_enabled) {
                        document.getElementById("allincall-minimize-popup").style.display = "flex";
                        if (window.disable_auto_popup_minimized && get_cookie('is_bot_minimized') == 'true'){
                            document.getElementById("allincall-popup").style.display = "none";
                            document.getElementById("allincall-min-popup").style.display = "block";
                            document.getElementById("allincall-maximize-popup").style.display = "flex";
                            document.getElementById("allincall-minimize-popup").style.display = "none";
                            document.getElementById("allincall-maximize-popup-tooltip").style.visibility = "hidden";
                            document.getElementById("allincall-minimize-popup-tooltip").style.visibility = "hidden";
                            change_css_on_bot_minimization(BOT_POSITION)
                        }
                    }
                    document.getElementById("allincall-chat-box").style.display = "none";
                    document.getElementById("easychat-bot-close-button").style.display = "none";
                    
                }, 1000);
                easychat_page_category = "";
                easychat_form_assist_id = "";
                easychat_minimized_chatbot = false;
                if (is_form_assist == 'true') {
                    element_id = ""
                    window.starting_element = false
                    window.clearTimeout(auto_form_pop_timer)
                    window.clearTimeout(timer);
                    timer_is_on = 0
                    check_user_activity_status()
                }
            }

            if (event.data == "share-screen") {
                share_screen();
            }

            if (is_form_assist == 'true') {
                if (event.data == 'stop-form-assist') {
                    clearTimeout(timer);
                    stop_form_assist = true
                    easychat_form_assist_id = "";
                    stop_user_activity_status();
                }
            }

            if (event.data.event_id == "update-form-assist-language-objects") {

                bot_id = event.data.data.bot_id;
                selected_language = event.data.data.selected_language;
                get_language_updated_form_assist_items(bot_id , selected_language);

            }

            if(event.data.event_id === "update_livechat_unload_event_flag") {
                setInterval(function() {
                    localStorage.setItem("myUnloadEventFlag", new Date().getTime());
                }, 1000);

            }

            if(event.data.event_id === "send_livechat_unload_event_flag") {
                document.getElementById("allincall-chat-box").contentWindow.postMessage({
                    event_id: 'livechat_unload_event_flag',
                    data: localStorage.getItem("myUnloadEventFlag"),
                }, "*")  
            }

        } else {
            // The data hasn't been sent from your site! 
            // Be careful! Do not use it. 
            return;
        }

    });
}

function change_css_on_bot_minimization(bot_position) {

    var greeting_bubble = false
    if(document.getElementsByClassName("greeting-bubble-notofication-wrapper").length > 0) {
        greeting_bubble = true
    }

    var new_notification_div = false
    if(document.getElementsByClassName("new-notification-div").length > 0) {
        new_notification_div = true
    }

        if(bot_position == "bottom-right"  || bot_position == "right") {

            if (greeting_bubble) {           
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.bottom = "80px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.right = "110px"
                document.getElementById("allincall-notification-count").style.right = "0px" 
            } 

            if (new_notification_div) {

                document.getElementsByClassName("new-notification-div")[0].style.top = "-50px"
                document.getElementsByClassName("new-notification-div")[0].style.right = "-20px"

            }
            
        } else if(bot_position == "bottom-left" || bot_position == "left") {
            
            if (greeting_bubble) { 
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.bottom = "80px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.left = "110px"
                document.getElementById("allincall-notification-count").style.left = "0px"  
            }

            if (new_notification_div) {

                document.getElementsByClassName("new-notification-div")[0].style.top = "-50px"
                document.getElementsByClassName("new-notification-div")[0].style.right = "-30px"
                
            }

        } else if(bot_position == "top-left") {
            
            if (greeting_bubble) { 
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.top = "60px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.left = "90px"
                document.getElementById("allincall-notification-count").style.left = "0px"  
            }

            if (new_notification_div) {
                document.getElementsByClassName("new-notification-div")[0].style.top = "35px"
                document.getElementsByClassName("new-notification-div")[0].style.left = "42px"  
            }

        } else if(bot_position == "top-right") {

            if (greeting_bubble) { 
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.top = "60px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.right = "90px" 
                document.getElementById("allincall-notification-count").style.right = "0px"   
            }

            if (new_notification_div) {
                document.getElementsByClassName("new-notification-div")[0].style.top = "35px"
                document.getElementsByClassName("new-notification-div")[0].style.right = "42px" 
            }

        }
}

function change_css_on_bot_maximization(bot_position) {

    var greeting_bubble = false
    if(document.getElementsByClassName("greeting-bubble-notofication-wrapper").length > 0) {
        greeting_bubble = true
    }

    var new_notification_div = false
    if(document.getElementsByClassName("new-notification-div").length > 0) {
        new_notification_div = true
    }
    
        if(bot_position == "bottom-right"  || bot_position == "right") {
            
            if (greeting_bubble) {
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.bottom = "181px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.right = "31px"
                document.getElementById("allincall-notification-count").style.right = "9px" 
            } 

            if (new_notification_div) {
                document.getElementsByClassName("new-notification-div")[0].style.top = "-40px"
                document.getElementsByClassName("new-notification-div")[0].style.right = "0px"
            }
            
            
        } else if(bot_position == "bottom-left" || bot_position == "left") {
            if (greeting_bubble) {

                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.bottom = "181px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.left = "25px"
                document.getElementById("allincall-notification-count").style.left = "4px" 
            } 

            if (new_notification_div) {
                document.getElementsByClassName("new-notification-div")[0].style.top = "-40px"
                document.getElementsByClassName("new-notification-div")[0].style.right = "0px"
            }

        } else if(bot_position == "top-left") {

            if (greeting_bubble) {
            
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.top = "169px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.left = "25px"
                document.getElementById("allincall-notification-count").style.left = "4px"   
            } 

            if (new_notification_div) {
                document.getElementsByClassName("new-notification-div")[0].style.top = "100px"
                document.getElementsByClassName("new-notification-div")[0].style.left = "100px"
            }

        } else if(bot_position == "top-right") {

            if (greeting_bubble) {

                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.top = "169px"
                document.getElementsByClassName("greeting-bubble-notofication-wrapper")[0].style.right = "28px"
                document.getElementById("allincall-notification-count").style.right = "9px"   
            }

            if (new_notification_div) {
                document.getElementsByClassName("new-notification-div")[0].style.top = "100px"
                document.getElementsByClassName("new-notification-div")[0].style.right = "100px"

            }

        }
    
}

function get_popup_id_and_classes(bot_position) {
    var ids_and_classes = []
    ids_and_classes[0] = "allincall-popup-wrapper"
    if(bot_position == "bottom-right"  || bot_position == "right") {

        ids_and_classes[1] = "bottom-right-position-wrapper"

    } else if(bot_position == "bottom-left" || bot_position == "left") {

        ids_and_classes[1] = "bottom-left-position-wrapper"

    } else if(bot_position == "top-left") {

        ids_and_classes[1] = "top-left-position-wrapper"

    } else if(bot_position == "top-right") {

        ids_and_classes[1] = "top-right-position-wrapper"

    } 

    ids_and_classes[2] = "allincall-popup-image-icon-wrapper"
    ids_and_classes[3] = "greeting-bubble-notofication-wrapper"
    return ids_and_classes
}


function trigger_autopopup_functionality(auto_pop_up_timer, auto_popup_type) {
    if (document.getElementById("allincall-chat-box").style.display == "block") {
        return;
    }
    if(auto_popup_type == "1"){
        auto_popup = setTimeout(function(e) {
        document.getElementById("allincall-popup").click();
        }, auto_pop_up_timer * 1000)
    }
    else if(auto_popup_type == "2" || auto_popup_type == "3"){
        auto_popup = setTimeout(function(e) {
            if(auto_popup_type == "2")
            document.getElementById("allincall-notification-count").style.display="flex"
            document.getElementById("notification-message-div").style.display="block"
            if(BOT_POSITION.indexOf("top") != -1 && document.getElementById("notification-message-div").parentNode.className.indexOf("greeting") != -1) {
                document.getElementById("notification-message-div").style.display="flex"
            }
        }, auto_pop_up_timer * 1000)
    }
}

function close_chatbot_animation() {
    var chat_box_window = document.getElementById("allincall-chat-box");
    try {
        chat_box_window.classList.remove("animate__animated")
        chat_box_window.classList.remove("animate__slideInUp")
        if (BOT_POSITION == "bottom-right") {
            chat_box_window.classList.remove("allincall-scale-out-br")
        } else if (BOT_POSITION == "bottom-left") {
            chat_box_window.classList.remove("allincall-scale-out-bl")
        }
    } catch (err) {}
    chat_box_window.className += "animate__animated animate__slideOutDown"

}

function send_message_into_allincall_chatbot_window(message) {
    var is_visible = true;
    if (document.getElementById("allincall-chat-box").style.display != "block") {
        //document.getElementById("allincall-popup").click();
        is_visible = false;
    }

    if (is_visible) {
        allincall_chat_window = document.getElementById("allincall-chat-box").contentWindow;
        allincall_chat_window.postMessage(message, SERVER_URL);
    } else {
        setTimeout(function(e) {
            allincall_chat_window = document.getElementById("allincall-chat-box").contentWindow;
            allincall_chat_window.postMessage(message, SERVER_URL);
        }, 2000);
    }
}

function hide_notification() {
    document.getElementById("chatbox-notification").style.display = "none";
    document.getElementById("cross-chatbox-notification").remove();
}

function show_cross() {
    try {
        document.getElementById("cross-chatbox-notification").style.display = "block";
    } catch (err) {}
}

function dont_show_cross() {
    try {
        document.getElementById("cross-chatbox-notification").style.display = "none";
    } catch (err) {}
}

function open_up_bot() {
    document.getElementById("allincall-popup").click();
}

function open_up_bot_by_greeting() {
    save_bubble_click_info("Greeting bubble", "0");
    document.getElementById("allincall-popup").click();
}

function minimize_chatbot_animation() {
    var chat_box_window = document.getElementById("allincall-chat-box");
    try {
        chat_box_window.classList.remove("animate__animated")
        chat_box_window.classList.remove("animate__slideInUp")
        chat_box_window.classList.remove("animate__animated")
        chat_box_window.classList.remove("animate__slideOutDown")
    } catch (err) {}
    if (BOT_POSITION == "bottom-right") {
        chat_box_window.className += "allincall-scale-out-br";
    } else if (BOT_POSITION == "bottom-left") {
        chat_box_window.className += "allincall-scale-out-bl";
    }
    

}
function hide_auto_pop_up_notification_text(){
    document.getElementById("notification-message-div").style.display="none";
    if(document.getElementById("allincall-notification-count")) {
        document.getElementById("allincall-notification-count").style.display="none";
    }
    is_greeting_bubble_closed = true
    set_auto_popup_not_required_cookie()
    cancel_text_to_speech();
}

function set_auto_popup_not_required_cookie() {
    document.cookie = "is_auto_popup_required" + "=false;path = / ; SameSite=None; Secure ";
}

function open_greeting_intents(thiselem, intent_pk){
    easychat_intent_name = thiselem.innerText
    is_initial_trigger_intent = true
    save_bubble_click_info(easychat_intent_name, intent_pk);
    document.getElementById("allincall-popup").click();
}

function save_bot_click_count(){
    var json_string = JSON.stringify({
    bot_id: BOT_ID,
    bot_web_page: window.location.href,
    web_page_source: web_page_source,
    });

    json_string = encrypt_variable(json_string);
    json_string = encodeURIComponent(json_string);
    var params = 'json_string=' + json_string;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", SERVER_URL + "/chat/save-bot-click-count/", true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
        }
    }
    xhttp.send(params);
}

function custom_decrypt(msg_string) {

    var payload = msg_string.split(".");
    var key = payload[0];
    var decrypted_data = payload[1];
    var decrypted = EasyChatCryptoJS.AES.decrypt(decrypted_data, EasyChatCryptoJS.enc.Utf8.parse(key), { iv: EasyChatCryptoJS.enc.Base64.parse(payload[2]) });
    return decrypted.toString(EasyChatCryptoJS.enc.Utf8);
}

///////////////////////////////////SUGGESTIONS LOADING START/////////////////////////////////////////////////
//  commented this code and moved to bot_suggestion.js 
// function load_storage(){
//     if (window.localStorage['word_mapper_list'] != null) {
//             window.localStorage.removeItem('word_mapper_list');
//             window.localStorage.removeItem('autocorrect_bot_replace')
//     }
//     delete_messages_from_local(table_name)
//     open_local_db()
// }

// function open_local_db() {
//     window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
//     window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.msIDBTransaction || {READ_WRITE: "readwrite"};
//     window.IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange || window.msIDBKeyRange;

//     if (!window.indexedDB) {
//         console.log("Your browser doesn't support a stable version of IndexedDB.");
//         is_indexed_db_supported = false;
//         return;
//     }

//     var openRequest = window.indexedDB.open(db_name, 1);

//     openRequest.onerror = function () {
//         is_indexed_db_supported = false        
//         console.error("Error", openRequest.error);
//     };

//     openRequest.onsuccess = function (event) {
//         db = event.target.result; 

//     };

//     openRequest.onupgradeneeded = function (event) {
//         db = event.target.result;

//         switch (event.oldVersion) {
//             case 0:
//                 //when user has no database
//                 suggestion_list_store = db.createObjectStore(table_name, { autoIncrement: true });
//                 suggestion_list_store.createIndex('table_index', 'table_index', { unique: false });
//         }
//     };
// }

// function get_object_store(store_name, mode) {
//     try{
//         var tx = db.transaction(store_name, mode);
//         return tx.objectStore(store_name);
//     }catch(err){
//         return -1
//     }
// }

// function add_message_to_local_db(data, store_name) {
//     var db_obj = get_object_store(store_name, 'readwrite');
//     var req;

//     try {
//         req = db_obj.add(data);
//     } catch (error) {
//         console.log(error);
//     }

//     req.onsuccess = function (evt) {
//         console.log("saved data to local db!");
//     };
//     req.onerror = function () {
//         console.error("error in saving data to local db: ", this.error);
//     };
// }

// function delete_messages_from_local(store_name) {
//     var suggestion_list_store = get_object_store(store_name, 'readwrite');
//     if(suggestion_list_store != -1){
//         var index = suggestion_list_store.index('table_index');
//         var key = IDBKeyRange.only(table_index);
//         index.openCursor(key, "next").onsuccess = function (event) {
//             var cursor = event.target.result;
//             if (cursor) {
//                 request = cursor.delete();

//                 request.onsuccess = function() {
//                     console.log('deleted message successfully!');
//                 }
//                 cursor.continue();
//             }
//         };
//     }
// }

// function get_suggestions() {
//     web_page = window.location.href
//     var json_string = JSON.stringify({
//         bot_id: BOT_ID,
//         count_of_chunk: count_of_chunk
//     });
//     json_string = encrypt_variable(json_string);
//     json_string = encodeURIComponent(json_string);

//     var xhttp = new XMLHttpRequest();
//     var params = 'json_string=' + json_string
//     xhttp.open("POST", SERVER_URL + "/chat/get-data-suggestions/", true);
//     xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//     xhttp.onreadystatechange = function() {
//         if (this.readyState == 4 && this.status == 200) {
//             response = JSON.parse(this.responseText);
//             response = custom_decrypt(response)
//             response = JSON.parse(response);
//             if (response["status"] == 200) {
//                 suggestion_list_response = JSON.parse(response["sentence_list"]);
//                 word_mapper_list = JSON.parse(response["word_mapper_list"]);
//                 total_length_of_chunk = response["total_length_of_chunk"]
//                 suggestion_list = suggestion_list.concat(suggestion_list_response)
//                 delete_messages_from_local(table_name)
//                 suggestion_list_dict = {
//                     'table_index': table_index,
//                     'suggestion_list': suggestion_list,
//                     }
//                 add_message_to_local_db(suggestion_list_dict,table_name)
//                 window.localStorage['word_mapper_list'] = JSON.stringify(word_mapper_list)
//                 document.getElementById("allincall-chat-box").contentWindow.postMessage({
//                     event_id: 'collect_from_local_storage' 
//                 }, "*")
//                 count_of_chunk = count_of_chunk + 1
//                 if (total_length_of_chunk > 1 && count_of_chunk != total_length_of_chunk){
//                     get_suggestions()
//                 }
                
//             }else{
//                 console.log("Error in getting suggestions")
//             }
//         }
//     }
//     xhttp.send(params);
// }
///////////////////////////////////SUGGESTIONS LOADING END/////////////////////////////////////////////////

////////// to check if location coming is of the form /chat/bot/?id /////////////////////

function correct_path_of_bot_for_autopopup(){
    window_location_and_parameters = window.location.pathname + window.location.search
    if (window_location_and_parameters.indexOf("/chat/bot/?id=") !== -1 || allowed_hosts_list.indexOf(window.location.hostname) == -1){
        return true;
    }
    return false;
}

//////////////////////////////////////////////// end /////////////////////////////////

///////// Add Save Bubble click count info /////////

function save_bubble_click_info(bubble_name, intent_pk){
    let selected_language = get_easychat_selected_language()
    var json_string = JSON.stringify({
    bot_id: BOT_ID,
    bubble_name: bubble_name,
    selected_language: selected_language,
    intent_pk: intent_pk,
    });

    json_string = encrypt_variable(json_string);
    json_string = encodeURIComponent(json_string);
    var params = 'json_string=' + json_string;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", SERVER_URL + "/chat/save-bubble-click-info/", true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
        }
    }
    xhttp.send(params);
}

////// End Save bubble click count info /////////////

///// Add external trigger intent function /////

function trigger_chatbot_query(intent_info) {

    if (easychat_minimized_chatbot){
        document.getElementById("allincall-popup").click();
        document.getElementById("allincall-chat-box").contentWindow.postMessage({
            event_id: 'trigger-external-intent',
            data: intent_info
        }, "*")
    } else if (document.getElementById("allincall-chat-box").style.display == "none"){
        external_trigger_intent_info = intent_info;
        document.getElementById("allincall-popup").click();
    } else {
        document.getElementById("allincall-chat-box").contentWindow.postMessage({
            event_id: 'trigger-external-intent',
            data: intent_info
        }, "*")
    }

}

///// End external trigger intent function /////

function update_form_assist_intent_bubbels(){

    for (var intent_pk in form_assist_intent_bubble) {

        let elemens = document.querySelectorAll(".notification-intent-message-bubble.form-assist-intent-bubble")
        for(let i=0; i<elemens.length;i++){
            elem = elemens[i]
            if(elem && (elem.id == intent_pk)){
                elem.innerText = form_assist_intent_bubble[intent_pk]
            }
        }

    } 
    
}

function update_form_assist_auto_pop_up_text(){
    if(form_assist_intent_bubble_type == "1"){
        // $("#form-assist-pop-up-text-for-type-1").html(window.form_assist_auto_pop_text)
        document.getElementById('form-assist-pop-up-text-for-type-1').innerHTML = window.form_assist_auto_pop_text 

    }

    else if(form_assist_intent_bubble_type == "2"){
        // $("#intent-bubble-greeting-message span").html(window.form_assist_auto_pop_text )
        var elem = document.querySelector("#intent-bubble-greeting-message span")
        elem.innerText = window.form_assist_auto_pop_text
    }
}

function get_language_updated_form_assist_items(bot_id , selected_language){


    var json_string = JSON.stringify({
        bot_id: bot_id,
        selected_language: selected_language,
    });
    json_string = encrypt_variable(json_string);
    json_string = encodeURIComponent(json_string);

    var xhttp = new XMLHttpRequest();
    var params = 'json_string=' + json_string
    xhttp.open("POST",  SERVER_URL + "/chat/get-language-updated-form-assist-details/", true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
            response = custom_decrypt(response)
            response = JSON.parse(response);
            if (response['status'] == 200) {

                window.is_form_assist_auto_pop_allowed = response.is_form_assist_auto_pop_allowed

                if(is_form_assist_auto_pop_allowed == true){

                    if( "form_assist_auto_pop_text" in response){

                        window.form_assist_auto_pop_text = response.form_assist_auto_pop_text;

                        update_form_assist_auto_pop_up_text();

                    }
                    if( "form_assist_intent_bubble" in response){
                        window.form_assist_intent_bubble = JSON.parse(response.form_assist_intent_bubble);

                        update_form_assist_intent_bubbels();
                    }
                    if( "form_assist_intent_responses_dict" in response){
                        window.form_assist_intent_responses_dict = JSON.parse(response.form_assist_intent_responses_dict);
                    }

                   
                }
            
            }
        }
    }
    xhttp.send(params);
}

function connect_with_cobrowse_agent(username, phone, livechat_session_id, cobrowsing_meeting_id, assigned_agent_username) {
    var title = window.location.href;
    if (document.querySelector("title") != null) {
        title = document.querySelector("title").innerHTML;
    }
    var description = "";
    if (document.querySelector("meta[name=description]") != null && document.querySelector("meta[name=description]") != undefined) {
        description = document.querySelector("meta[name=description]").content;
    }
    var url = window.location.href;
    var request_id = livechat_session_id;

    // var easyassist_customer_id = get_easyassist_cookie("easyassist_customer_id");
    // if (easyassist_customer_id == null || easyassist_customer_id == undefined) {
    //     easyassist_customer_id = "None";
    // }

    var easyassist_customer_id = "None";

    var selected_language = -1;
    let selected_product_category = -1;

    // var browsing_time_before_connect_click = get_easyassist_cookie("easyassist_customer_browsing_time");
    // if(browsing_time_before_connect_click == null || browsing_time_before_connect_click == undefined){
    //     browsing_time_before_connect_click = 0;
    // }

    var browsing_time_before_connect_click = 0;

    var longitude = null;
    var latitude = null;

    json_string = JSON.stringify({
        "request_id": request_id,
        "name": username,
        "mobile_number": phone,
        "longitude": longitude,
        "latitude": latitude,
        "selected_language": selected_language,
        "selected_product_category": selected_product_category,
        "active_url": window.location.href,
        "customer_id": easyassist_customer_id,
        "browsing_time_before_connect_click": browsing_time_before_connect_click,
        "is_request_from_greeting_bubble": false,
        "meta_data": {
            "product_details": {
                "title": title,
                "description": description,
                "url": url
            }
        },
        "is_livechat_request": true,
        "assigned_agent_username": assigned_agent_username,
    });

    encrypted_data = encrypt_variable(json_string);
    encrypted_data = {
        "Request": encrypted_data
    };
    var params = JSON.stringify(encrypted_data);

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", EASYASSIST_HOST_PROTOCOL + "://" + EASYASSIST_COBROWSE_HOST + "/easy-assist/initialize/", true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.setRequestHeader('X-AccessToken', parent.window.EASYASSIST_COBROWSE_META.access_token);
    xhttp.onreadystatechange = function() {

        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
            response = custom_decrypt(response.Response);
            response = JSON.parse(response);
            // easyassist_clear_local_storage();

            if (response.status == 200) {
                console.log(response);
                set_easyassist_cookie("easyassist_session_created_on", "request");
                if(get_easyassist_cookie("easyassist_session_id") != undefined){
                    easyassist_terminate_cobrowsing_session(show_message=false)
                }

                set_easyassist_cookie("easyassist_session_id", response.session_id);
                set_easyassist_cookie("easyassist_request_timestamp", Date.now())

                document.getElementById("allincall-chat-box").contentWindow.postMessage({
                    event_id: 'cobrowse-session-id',
                    data: response.session_id,
                }, "*")

                send_cobrowsing_status_to_server('accepted', response.session_id, livechat_session_id, cobrowsing_meeting_id)

                if(localStorage.getItem("easyassist_session") == null){
                    var local_storage_json_object = {};
                    local_storage_json_object[response.session_id] = {};
                    localStorage.setItem("easyassist_session", JSON.stringify(local_storage_json_object));
                }

                set_easyassist_cookie("easyassist_cobrowsing_allowed", "true");

                if(EASYASSIST_COBROWSE_META.no_agent_connects_toast) {
                    easyassist_initiate_connection_with_timer_modal();
                } else {
                    if (EASYASSIST_COBROWSE_META.show_connect_confirmation_modal) {
                        easyassist_show_connection_modal();
                    }    
                }
                easyassist_close_browsing_modal();

            } else if (response.status == 103) {

                document.getElementById("modal-cobrowse-connect-error").innerHTML = "Please enter code shared by our agent";

            } else {

                easyassist_close_browsing_modal();
                easyassist_show_function_fail_modal(code=635);
                console.error(response);

            }
        } else if (this.readyState == 4) {
            easyassist_close_browsing_modal();
            easyassist_show_function_fail_modal(code=636);
        }
        document.getElementById("easyassist-co-browsing-connect-button").disabled = false;
    }
    xhttp.send(params);
}

function send_cobrowsing_status_to_server(status, cobrowse_session_id, livechat_session_id, cobrowsing_meeting_id) {
    json_string = {
        'meeting_id': cobrowsing_meeting_id,
        'livechat_session_id': livechat_session_id,
        'request_type': status,
        'cobrowse_session_id': cobrowse_session_id,
    }
    json_string = JSON.stringify(json_string);
    json_string = encrypt_variable(json_string);
    json_string = encodeURIComponent(json_string);

    var xhttp = new XMLHttpRequest();
    var params = "json_string=" + json_string;
    xhttp.open("POST", SERVER_URL + '/livechat/manage-cobrowsing-request/', true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            response = this.response;
            response = JSON.parse(response);
            response = custom_decrypt(response);
            response = JSON.parse(response);
            if (response["status_code"] == 200 || response["status_code"] == "200") {
                console.log("status saved");
            }
        }
    };
    xhttp.send(params);
}
