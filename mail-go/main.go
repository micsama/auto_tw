package main

import (
	"fmt"
	"net/smtp"
	"os"
)

const (
	// 邮件服务器地址
	SMTP_MAIL_HOST = "smtp.163.com"
	// 端口
	SMTP_MAIL_PORT = "25"
	// 发送邮件用户账号
	SMTP_MAIL_USER = "micsamamsg@163.com"
	// 发送邮件昵称
	SMTP_MAIL_NICKNAME = "SMTPMail"
)

func SendMail(address string, subject string, body string, passwd string) (err error) {
	// 通常身份应该是空字符串，填充用户名.
	auth := smtp.PlainAuth("", SMTP_MAIL_USER, passwd, SMTP_MAIL_HOST)
	fmt.Printf("passwd: %v\n", passwd)
	contentType := "Content-Type: text/html; charset=UTF-8"
	if address != "@qq.mail" {
		s := fmt.Sprintf("To:%s\r\nFrom:%s<%s>\r\nSubject:%s\r\n%s\r\n\r\n%s",
			address, SMTP_MAIL_NICKNAME, SMTP_MAIL_USER, subject, contentType, body)
		msg := []byte(s)
		addr := fmt.Sprintf("%s:%s", SMTP_MAIL_HOST, SMTP_MAIL_PORT)
		err = smtp.SendMail(addr, auth, SMTP_MAIL_USER, []string{address}, msg)
		if err != nil {
			return err
		}
	}
	return
}
func main() {
	fmt.Println(SendMail(os.Args[1], os.Args[2], os.Args[3], os.Args[4]))
}
