package com.example.backend.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {

    private String id;

    private String fullName;

    private String email;

    private String password;

    private String aadharNumber;

    private Role role;

    private String createdAt = java.time.LocalDateTime.now().toString();
}
