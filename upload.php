<?php
// 데이터 수신
$data = json_decode(file_get_contents("php://input"), true);

if (isset($data['image'])) {
    $imgData = $data['image'];

    // Base64 형식에서 앞부분 제거
    $imgData = str_replace('data:image/png;base64,', '', $imgData);
    $imgData = str_replace(' ', '+', $imgData);
    $imgDecoded = base64_decode($imgData);

    // 파일 저장
    $filename = 'uploads/captured.png';
    if (!is_dir('uploads')) {
        mkdir('uploads', 0755, true);
    }

    if (file_put_contents($filename, $imgDecoded)) {
        echo "업로드 성공! 저장된 파일: $filename";
    } else {
        echo "업로드 실패";
    }
} else {
    echo "이미지 데이터가 없습니다.";
}
?>
