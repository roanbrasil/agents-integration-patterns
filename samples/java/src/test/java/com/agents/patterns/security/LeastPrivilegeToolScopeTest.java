package com.agents.patterns.security;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@ExtendWith(MockitoExtension.class)
class LeastPrivilegeToolScopeTest {

    @Test
    void allowedTool_executesSuccessfully() {
        LeastPrivilegeToolScope scope = new LeastPrivilegeToolScope(Set.of("read-file", "list-dir"));
        scope.registerHandler("read-file", args -> "Contents of " + args);

        String result = scope.callTool("read-file", "/etc/config.txt");

        assertThat(result).contains("Contents of /etc/config.txt");
    }

    @Test
    void blockedTool_throwsSecurityException() {
        LeastPrivilegeToolScope scope = new LeastPrivilegeToolScope(Set.of("read-file"));

        assertThatThrownBy(() -> scope.callTool("delete-file", "/important/data"))
                .isInstanceOf(SecurityException.class)
                .hasMessageContaining("delete-file")
                .hasMessageContaining("allowed scope");
    }
}
