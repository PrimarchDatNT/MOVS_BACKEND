# sam-app

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

-   movisapi - Code for the application's MOVS function.
-   template.yaml - A template that defines the application's AWS resources.

# Deploy the sample application

**Trước khi deploy cần cài đặt các tool sau**

-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
-   [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

**Tiếp theo ta cần config AWS credential**

1. Đăng nhập AWS trên web và truy cập **Security credentials**
   ![1.](/images/1.png)
2. Kéo xuống dưới và tạo access key:
   ![2.](/images/2.png)
3. Chọn config: **Command Line Interface (CLI) -> Check "I understand..." -> Next -> Create access key.** Giữ nguyên màn hình AWS.
4. Mở file `C:\Users\[username]\.aws\credentials` và copy giá trị access key vừa tạo:

```bash
[default]
aws_access_key_id = ...
aws_secret_access_key = ...
```

5. Tạo default config trong file `C:\Users\[username]\.aws\config` với region Mumbai Ấn Độ:

```bash
[default]
region = ap-south-1
output = json
```

**Cấu trúc project SAM**

1. Default **samconfig.toml** default config. [Detail](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html)
2. File **template.yaml** cấu hình các tài nguyên sử dụng trên AWS.

-   Ví dụ `GetCateFunction` tương ứng với hàm `movisapi.get_detail_handler` và API `/getDetail`. Kèm theo đó là cấu hình về S3 và các policy.

3. File **requirements** chứa các thư viện cần được cài đặt để chạy lambda function.
4. Source code **movisapi.py** chứa các lambda handlers với đầu vào bao gồm `event` và `context`. VD: `def get_detail_handler(event, context):` cùng cách sử dụng như trong source code.

**Deploy project**

Để deploy project lên AWS chỉ cần chạy 2 câu lệnh sau:

```bash
sam build
sam deploy
```

Lệnh đầu tiên để build project. Lệnh thứ 2 sẽ nén project và đẩy lên AWS với các cấu hình sau:

-   **Stack Name**: Tên được deploy trên CloudFormation phải là duy nhất trong account và region.
-   **AWS Region**: Chọn region để deploy
-   **Confirm changes before deploy**: Manual review trước khi deploy
-   **Allow SAM CLI IAM role creation**: Tạo các IAM Roles cần thiết cho Lambda function
-   **Save arguments to samconfig.toml**: Lưu các config vào file .toml

Check API Gateway Endpoint URL ở phần output cuối command. Confige trong `Outputs` của file `template.yaml`

## Upload folder resource to S3

Nếu s3 ở chưa có file resource, upload resource lên S3:

```bash
aws s3 cp s3 cp .\resource\ s3://movis-data/resource/ --recursive
```

## Clean up

Để xóa project vừa tạo, run command sau:

```bash
sam delete --stack-name "sam-app"
```
