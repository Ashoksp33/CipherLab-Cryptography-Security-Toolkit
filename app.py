"""CipherLab: Interactive Information and Network Security Cryptography Toolkit.

Built with Streamlit for demonstration, education, and cryptanalysis.
"""

import pandas as pd
import streamlit as st

from ciphers import (
    aes_tool,
    affine,
    analysis,
    atbash,
    caesar,
    hashing,
    password_tools,
    playfair,
    railfence,
    rsa_tool,
    vigenere,
)

# Page configuration
st.set_page_config(
    page_title="CipherLab | Cryptography Toolkit",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State
if "rsa_private_pem" not in st.session_state:
    st.session_state.rsa_private_pem = ""
if "rsa_public_pem" not in st.session_state:
    st.session_state.rsa_public_pem = ""


def render_sidebar():
    """Render sidebar navigation and project metadata."""
    st.sidebar.title("🔐 CipherLab")
    st.sidebar.caption("INS Mini Project Cryptography Suite")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home / About",
            "📜 Classical Ciphers",
            "🛡️ AES Encryption",
            "🔑 RSA & Digital Signatures",
            "⚡ Hashing & HMAC",
            "🔍 File Integrity Checker",
            "🎲 Password Tools",
            "📊 Frequency Analysis",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        **System Status**: 🟢 Online  
        **Python**: 3.10+ | **UI**: Streamlit  
        **Library**: `cryptography`
        """
    )
    return page


# =====================================================================
# PAGE 1: HOME / ABOUT
# =====================================================================
def page_home():
    st.title("🔐 CipherLab: Cryptography Toolkit")
    st.subheader("Information & Network Security (INS) Mini Project")

    st.markdown(
        """
        **CipherLab** is an interactive, modular cryptography learning lab and toolkit designed to bridge
        theoretical information security concepts with hands-on, practical implementation.
        From foundational classical substitution and transposition techniques to modern NIST-approved
        cryptographic primitives (AES-GCM, RSA-PSS, SHA-256), CipherLab demonstrates the mechanics,
        strengths, and vulnerabilities of cryptographic algorithms.
        """
    )

    st.markdown("### 🎯 Mapping to the CIA Triad")
    st.markdown(
        "The **CIA Triad** (Confidentiality, Integrity, and Authenticity/Availability) forms the foundation of modern cybersecurity:"
    )

    cia_data = [
        {
            "Security Pillar": "🔒 Confidentiality",
            "Objective": "Ensure sensitive data is inaccessible to unauthorized entities.",
            "CipherLab Implementation": "Caesar, Vigenère, Playfair, Rail Fence, Affine, Atbash, AES-256-GCM, RSA-OAEP",
        },
        {
            "Security Pillar": "🛡️ Integrity",
            "Objective": "Detect unauthorized data tampering or corruption during transit or storage.",
            "CipherLab Implementation": "SHA-256, SHA-512, MD5, SHA-1, Chunked File Integrity Verification, HMAC-SHA256",
        },
        {
            "Security Pillar": "✍️ Authenticity & Non-Repudiation",
            "Objective": "Prove message origin and prevent senders from denying genuine messages.",
            "CipherLab Implementation": "RSA-PSS Digital Signatures, HMAC-SHA256 Secret Authentication Codes",
        },
    ]
    st.table(pd.DataFrame(cia_data))

    st.markdown("### 🧰 Toolkit Modules Overview")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            - **Classical Ciphers**:
              - Caesar (with 25-shift brute force engine)
              - Vigenère (polyalphabetic substitution)
              - Playfair (5x5 digraph key matrix)
              - Rail Fence (zig-zag transposition)
              - Affine ($E(x) = (ax + b) \\pmod{26}$)
              - Atbash (self-reciprocal mirror)
            - **Modern Symmetric**:
              - AES-256-GCM with PBKDF2HMAC (600,000 rounds)
              - Text & Streaming File encryption/decryption
            """
        )

    with col2:
        st.markdown(
            """
            - **Modern Asymmetric**:
              - 2048-bit RSA Key Pair Generation
              - RSA-OAEP encryption & decryption
              - RSA-PSS Digital Signatures & verification
            - **Integrity & Cryptanalysis**:
              - Text & 8 KB chunked file hashing
              - Automated Hash matching & algorithm auto-detection
              - Shannon Entropy & Password Generator
              - Monofrequency analysis cryptanalysis chart
            """
        )

    st.info("💡 Tip: Use the sidebar navigation on the left to explore each cryptographic tool.")


# =====================================================================
# PAGE 2: CLASSICAL CIPHERS
# =====================================================================
def page_classical_ciphers():
    st.title("📜 Classical Ciphers")
    st.caption("Historical substitution and transposition ciphers with interactive visualizations.")

    cipher_choice = st.selectbox(
        "Select Cipher",
        ["Caesar", "Vigenère", "Playfair", "Rail Fence", "Affine", "Atbash"],
    )

    action = st.radio("Operation", ["Encrypt", "Decrypt"], horizontal=True)
    text_input = st.text_area(
        "Input Text",
        value="Information Security 2026",
        height=100,
        placeholder="Enter text to process...",
    )

    # Dynamic Key Configuration
    key_val = None
    if cipher_choice == "Caesar":
        key_val = st.number_input("Shift Key (integer)", value=3, step=1)
    elif cipher_choice == "Vigenère":
        key_val = st.text_input("Alphabetic Keyword", value="KEYWORD")
    elif cipher_choice == "Playfair":
        key_val = st.text_input("Matrix Keyword", value="MONARCHY")
        st.caption("Note: Decryption recovers the normalized plaintext (uppercase, J->I, padded with X/Q).")
    elif cipher_choice == "Rail Fence":
        key_val = st.number_input("Number of Rails (>= 2 and < text length)", value=3, min_value=2, step=1)
    elif cipher_choice == "Affine":
        col_a, col_b = st.columns(2)
        with col_a:
            a_val = st.number_input("Multiplier 'a' (must be coprime with 26)", value=5, min_value=1, step=2)
        with col_b:
            b_val = st.number_input("Shift 'b' (integer)", value=8, step=1)
        key_val = (int(a_val), int(b_val))
    elif cipher_choice == "Atbash":
        st.info("Atbash is a fixed reciprocal cipher: A ↔ Z, B ↔ Y. No key required.")
        key_val = None

    if st.button(f"Execute {action}", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ Please provide input text.")
            return

        try:
            result = ""
            if cipher_choice == "Caesar":
                result = caesar.encrypt(text_input, int(key_val)) if action == "Encrypt" else caesar.decrypt(text_input, int(key_val))
            elif cipher_choice == "Vigenère":
                result = vigenere.encrypt(text_input, str(key_val)) if action == "Encrypt" else vigenere.decrypt(text_input, str(key_val))
            elif cipher_choice == "Playfair":
                result = playfair.encrypt(text_input, str(key_val)) if action == "Encrypt" else playfair.decrypt(text_input, str(key_val))
            elif cipher_choice == "Rail Fence":
                result = railfence.encrypt(text_input, int(key_val)) if action == "Encrypt" else railfence.decrypt(text_input, int(key_val))
            elif cipher_choice == "Affine":
                result = affine.encrypt(text_input, key_val) if action == "Encrypt" else affine.decrypt(text_input, key_val)
            elif cipher_choice == "Atbash":
                result = atbash.encrypt(text_input) if action == "Encrypt" else atbash.decrypt(text_input)

            st.success(f"✅ {action}ion Successful:")
            st.code(result, language="text")

        except ValueError as e:
            st.error(f"❌ Input Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")

    # Visualizations & Educational Tools
    st.markdown("---")
    if cipher_choice == "Playfair":
        with st.expander("🔍 View 5x5 Playfair Key Matrix", expanded=True):
            if key_val:
                try:
                    matrix = playfair.generate_matrix(str(key_val))
                    df_matrix = pd.DataFrame(matrix, columns=[f"Col {i+1}" for i in range(5)], index=[f"Row {i+1}" for i in range(5)])
                    st.table(df_matrix)
                except Exception as e:
                    st.caption(f"Enter a valid keyword to render the matrix ({e}).")

    elif cipher_choice == "Rail Fence":
        with st.expander("🔍 View Rail Fence Zig-Zag Grid", expanded=True):
            if text_input and key_val and isinstance(key_val, int) and 2 <= key_val < len(text_input):
                try:
                    grid = railfence.get_grid(text_input, key_val)
                    grid_lines = ["".join(row) for row in grid]
                    st.code("\n".join(grid_lines), language="text")
                except Exception as e:
                    st.caption(f"Unable to render grid: {e}")

    elif cipher_choice == "Caesar":
        with st.expander("🔨 Caesar Brute-Force Cracking Engine (All 25 Shifts)"):
            if text_input.strip():
                try:
                    candidates = caesar.brute_force(text_input)
                    df_bf = pd.DataFrame(candidates, columns=["Shift (+/-)", "Decrypted Plaintext Candidate"])
                    st.dataframe(df_bf, use_container_width=True)
                except Exception as e:
                    st.caption(f"Brute force failed: {e}")
            else:
                st.caption("Enter ciphertext above to brute-force all shifts.")

    with st.expander("ℹ️ Algorithm Details & Cryptographic Principles"):
        if cipher_choice == "Caesar":
            st.markdown("Caesar is a monoalphabetic substitution cipher: $C_i = (P_i + k) \\pmod{26}$. Easily broken via 25 brute-force checks or frequency analysis.")
        elif cipher_choice == "Vigenère":
            st.markdown("Vigenère uses repeated polyalphabetic keys: $C_i = (P_i + K_{i \\bmod m}) \\pmod{26}$. Flattened by Kasiski examination and index of coincidence.")
        elif cipher_choice == "Playfair":
            st.markdown("Playfair encrypts digraphs using a 5x5 key matrix. Letters 'I' and 'J' share a cell. Limits letter-frequency attacks by diffusing single-letter frequencies into 600 possible digraphs.")
        elif cipher_choice == "Rail Fence":
            st.markdown("A transposition cipher that rearranges character positions in a zig-zag wave across $k$ rails. Character frequencies remain identical to the plaintext.")
        elif cipher_choice == "Affine":
            st.markdown("Affine combines multiplicative and additive modular arithmetic: $E(x) = (ax + b) \\pmod{26}$. Invertible only when $\\gcd(a, 26) = 1$.")
        elif cipher_choice == "Atbash":
            st.markdown("Atbash maps the $i$-th letter to the $(26 - i + 1)$-th letter: $E(x) = (25 - x) \\pmod{26}$. Self-inverting cipher.")


# =====================================================================
# PAGE 3: AES ENCRYPTION (AES-256-GCM)
# =====================================================================
def page_aes_encryption():
    st.title("🛡️ AES-256-GCM Authenticated Encryption")
    st.caption("NIST-standard symmetric authenticated encryption with PBKDF2HMAC key derivation.")

    with st.expander("ℹ️ How AES-256-GCM & PBKDF2 Protect Your Data", expanded=False):
        st.markdown(
            """
            - **Key Derivation (PBKDF2HMAC-SHA256)**: Converts human passphrases into 256-bit cryptographic keys using **600,000 iterations** and a **16-byte cryptographically random salt** (preventing rainbow tables and GPU attacks).
            - **Authenticated Encryption (GCM Mode)**: Combines Galois Counter Mode with GMAC to provide **both confidentiality and data integrity** (tampering detection).
            - **Format**: `base64(salt [16 bytes] + nonce [12 bytes] + ciphertext_with_tag)`.
            """
        )

    tab_text, tab_file = st.tabs(["🔤 Text Encryption", "📁 File Encryption"])

    # Text Tab
    with tab_text:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Encrypt Text")
            aes_plain = st.text_area("Plaintext", placeholder="Enter message to encrypt...", key="aes_plain_in")
            aes_pass_enc = st.text_input("Encryption Password", type="password", key="aes_pass_enc_in")
            if st.button("Encrypt Text", type="primary", key="aes_enc_btn"):
                if not aes_plain.strip() or not aes_pass_enc:
                    st.warning("⚠️ Both plaintext and password are required.")
                else:
                    try:
                        with st.spinner("Deriving 256-bit key (600,000 PBKDF2 rounds) & encrypting..."):
                            token = aes_tool.encrypt_text(aes_plain, aes_pass_enc)
                        st.success("✅ Encrypted Successfully:")
                        st.code(token, language="text")
                    except Exception as e:
                        st.error(f"❌ Encryption Error: {str(e)}")

        with col2:
            st.subheader("Decrypt Text")
            aes_cipher = st.text_area("Base64 Ciphertext Token", placeholder="Paste base64 ciphertext token...", key="aes_cipher_in")
            aes_pass_dec = st.text_input("Decryption Password", type="password", key="aes_pass_dec_in")
            if st.button("Decrypt Text", type="primary", key="aes_dec_btn"):
                if not aes_cipher.strip() or not aes_pass_dec:
                    st.warning("⚠️ Both ciphertext token and password are required.")
                else:
                    try:
                        with st.spinner("Deriving key & verifying authentication tag..."):
                            recovered = aes_tool.decrypt_text(aes_cipher, aes_pass_dec)
                        st.success("✅ Decrypted Plaintext:")
                        st.code(recovered, language="text")
                    except ValueError as e:
                        st.error(f"❌ {str(e)}")
                    except Exception as e:
                        st.error(f"❌ {str(e)}")

    # File Tab
    with tab_file:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.subheader("Encrypt File to `.enc`")
            up_file = st.file_uploader("Choose a file to encrypt", key="aes_file_up")
            file_pass_enc = st.text_input("File Password", type="password", key="file_pass_enc")

            if st.button("Encrypt File", key="btn_enc_file"):
                if not up_file or not file_pass_enc:
                    st.warning("⚠️ Please upload a file and enter a password.")
                else:
                    try:
                        with st.spinner("Encrypting file with AES-256-GCM..."):
                            file_bytes = up_file.read()
                            encrypted_data = aes_tool.encrypt_bytes(file_bytes, file_pass_enc)
                        st.success(f"✅ Encrypted {len(file_bytes)} bytes -> {len(encrypted_data)} bytes (.enc)")
                        st.download_button(
                            label=f"⬇️ Download {up_file.name}.enc",
                            data=encrypted_data,
                            file_name=f"{up_file.name}.enc",
                            mime="application/octet-stream",
                        )
                    except Exception as e:
                        st.error(f"❌ File Encryption Failed: {str(e)}")

        with col_f2:
            st.subheader("Decrypt `.enc` File")
            up_enc_file = st.file_uploader("Upload an encrypted `.enc` file", key="aes_enc_file_up")
            file_pass_dec = st.text_input("Decryption Password", type="password", key="file_pass_dec")

            if st.button("Decrypt File", key="btn_dec_file"):
                if not up_enc_file or not file_pass_dec:
                    st.warning("⚠️ Please upload a `.enc` file and provide the password.")
                else:
                    try:
                        with st.spinner("Verifying GCM tag and decrypting file..."):
                            enc_bytes = up_enc_file.read()
                            decrypted_data = aes_tool.decrypt_bytes(enc_bytes, file_pass_dec)

                        out_name = up_enc_file.name[:-4] if up_enc_file.name.endswith(".enc") else f"decrypted_{up_enc_file.name}"
                        st.success(f"✅ Decrypted {len(decrypted_data)} bytes successfully!")
                        st.download_button(
                            label=f"⬇️ Download Decrypted File ({out_name})",
                            data=decrypted_data,
                            file_name=out_name,
                            mime="application/octet-stream",
                        )
                    except ValueError as e:
                        st.error(f"❌ {str(e)}")
                    except Exception as e:
                        st.error(f"❌ {str(e)}")


# =====================================================================
# PAGE 4: RSA & DIGITAL SIGNATURES
# =====================================================================
def page_rsa():
    st.title("🔑 RSA Public-Key Cryptography & Signatures")
    st.caption("2048-bit Asymmetric Cryptography (OAEP Encryption + PSS Digital Signatures).")

    tab_keys, tab_enc, tab_sig = st.tabs(["🔑 Key Management", "🔒 Encryption & Decryption", "✍️ Digital Signatures"])

    # 1. Key Management
    with tab_keys:
        st.subheader("2048-bit RSA Key Pair Generation")
        if st.button("Generate New Key Pair", type="primary"):
            with st.spinner("Generating 2048-bit RSA key pair with e=65537..."):
                priv, pub = rsa_tool.generate_key_pair()
                st.session_state.rsa_private_pem = priv
                st.session_state.rsa_public_pem = pub
                st.success("✅ New 2048-bit RSA Key Pair generated and stored in session!")

        st.warning(
            "⚠️ Security Notice: The private key is exported unencrypted strictly for academic/demo purposes. "
            "In production environments, private keys must be protected with passphrase encryption (e.g., BestAvailableEncryption) and stored in secure keystores/HSMs."
        )

        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.markdown("**Public Key (Shareable):**")
            st.text_area("Public Key PEM", value=st.session_state.rsa_public_pem, height=220, key="disp_pub_pem")
            if st.session_state.rsa_public_pem:
                st.download_button("⬇️ Download public_key.pem", data=st.session_state.rsa_public_pem, file_name="public_key.pem")

        with col_k2:
            st.markdown("**Private Key (Secret):**")
            st.text_area("Private Key PEM", value=st.session_state.rsa_private_pem, height=220, key="disp_priv_pem")
            if st.session_state.rsa_private_pem:
                st.download_button("⬇️ Download private_key.pem", data=st.session_state.rsa_private_pem, file_name="private_key.pem")

    # 2. Encryption / Decryption
    with tab_enc:
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.subheader("Encrypt with Public Key")
            msg_to_enc = st.text_area("Plaintext Message (Max 190 bytes)", placeholder="Enter short confidential message...", key="rsa_msg_enc")
            st.caption(f"Length: {len(msg_to_enc.encode('utf-8'))} / 190 bytes for RSA-2048 OAEP-SHA256")
            pub_key_input = st.text_area("Recipient's Public Key PEM", value=st.session_state.rsa_public_pem, height=140, key="rsa_pub_enc_field")

            if st.button("Encrypt with RSA", key="rsa_enc_btn"):
                if not msg_to_enc.strip() or not pub_key_input.strip():
                    st.warning("⚠️ Message and Public Key are required.")
                else:
                    try:
                        ct_b64 = rsa_tool.encrypt(msg_to_enc, pub_key_input)
                        st.success("✅ Ciphertext (Base64):")
                        st.code(ct_b64, language="text")
                    except ValueError as e:
                        st.error(f"❌ {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Encryption Error: {str(e)}")

        with col_e2:
            st.subheader("Decrypt with Private Key")
            ct_to_dec = st.text_area("Base64 Ciphertext", placeholder="Paste base64 ciphertext...", key="rsa_ct_dec")
            priv_key_input = st.text_area("Recipient's Private Key PEM", value=st.session_state.rsa_private_pem, height=140, key="rsa_priv_dec_field")

            if st.button("Decrypt with RSA", key="rsa_dec_btn"):
                if not ct_to_dec.strip() or not priv_key_input.strip():
                    st.warning("⚠️ Ciphertext and Private Key are required.")
                else:
                    try:
                        recovered = rsa_tool.decrypt(ct_to_dec, priv_key_input)
                        st.success("✅ Decrypted Plaintext:")
                        st.code(recovered, language="text")
                    except ValueError as e:
                        st.error(f"❌ {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Decryption Error: {str(e)}")

    # 3. Digital Signatures
    with tab_sig:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.subheader("1. Sign Message (Private Key)")
            doc_to_sign = st.text_area("Document / Message to Sign", value="Authorized Transfer: $5,000 to Alice", key="sig_doc_in")
            signer_priv = st.text_area("Signer's Private Key PEM", value=st.session_state.rsa_private_pem, height=130, key="sig_priv_in")

            if st.button("Generate Digital Signature", key="btn_sign"):
                if not doc_to_sign.strip() or not signer_priv.strip():
                    st.warning("⚠️ Message and Private Key are required.")
                else:
                    try:
                        signature = rsa_tool.sign(doc_to_sign, signer_priv)
                        st.success("✅ Digital Signature Generated (PSS-SHA256):")
                        st.code(signature, language="text")
                    except Exception as e:
                        st.error(f"❌ Signing Error: {str(e)}")

        with col_s2:
            st.subheader("2. Verify Signature (Public Key)")
            doc_to_verify = st.text_area("Original Document / Message", value="Authorized Transfer: $5,000 to Alice", key="sig_doc_verify")
            sig_to_verify = st.text_area("Digital Signature (Base64)", placeholder="Paste base64 signature...", key="sig_val_verify")
            signer_pub = st.text_area("Signer's Public Key PEM", value=st.session_state.rsa_public_pem, height=130, key="sig_pub_in")

            if st.button("Verify Digital Signature", key="btn_verify"):
                if not doc_to_verify.strip() or not sig_to_verify.strip() or not signer_pub.strip():
                    st.warning("⚠️ Message, Signature, and Public Key are all required.")
                else:
                    try:
                        is_valid = rsa_tool.verify(doc_to_verify, sig_to_verify, signer_pub)
                        if is_valid:
                            st.success("✅ SIGNATURE IS VALID! Authenticity and message integrity confirmed.")
                        else:
                            st.error("❌ SIGNATURE IS INVALID! Message was altered or signed by a different key.")
                    except Exception as e:
                        st.error(f"❌ Verification Error: {str(e)}")


# =====================================================================
# PAGE 5: HASHING & HMAC
# =====================================================================
def page_hashing():
    st.title("⚡ Cryptographic Hashing & HMAC")
    st.caption("One-way cryptographic hash functions and keyed message authentication codes.")

    st.warning(
        "⚠️ Educational & Security Notice: **MD5** and **SHA-1** are cryptographically broken due to practical collision attacks. "
        "They are included strictly for historical learning and legacy checksum validation. Use **SHA-256** or **SHA-512** for secure applications."
    )

    tab_text, tab_file, tab_hmac = st.tabs(["🔤 Text Hashing", "📁 File Hashing", "🔑 HMAC-SHA256"])

    with tab_text:
        text_to_hash = st.text_area("Text to Hash", value="Cryptography & Information Security", key="hash_text_in")
        algo = st.selectbox("Hash Algorithm", ["SHA-256", "SHA-512", "SHA-1", "MD5"], key="hash_algo_select")

        if st.button("Calculate Hash", key="btn_hash_txt"):
            try:
                digest = hashing.hash_text(text_to_hash, algo)
                st.success(f"✅ {algo} Digest:")
                st.code(digest, language="text")
                st.caption(f"Digest Length: {len(digest)} hex characters ({len(digest) * 4} bits)")
            except Exception as e:
                st.error(f"❌ Hashing Error: {str(e)}")

    with tab_file:
        hash_file_up = st.file_uploader("Upload File to Hash", key="hash_file_uploader")
        file_algo = st.selectbox("Hash Algorithm for File", ["SHA-256", "SHA-512", "SHA-1", "MD5"], key="file_algo_select")

        if st.button("Calculate File Hash", key="btn_hash_file"):
            if not hash_file_up:
                st.warning("⚠️ Please upload a file to hash.")
            else:
                try:
                    with st.spinner("Streaming file in 8 KB chunks to compute hash..."):
                        digest = hashing.hash_file(hash_file_up, file_algo)
                    st.success(f"✅ {file_algo} Hash for '{hash_file_up.name}':")
                    st.code(digest, language="text")
                    st.caption(f"File Size: {hash_file_up.size} bytes | Memory Footprint: Constant (8 KB buffer)")
                except Exception as e:
                    st.error(f"❌ File Hash Failed: {str(e)}")

    with tab_hmac:
        st.subheader("Keyed-Hash Message Authentication Code (HMAC-SHA256)")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            hmac_msg = st.text_area("Message", value="Invoice #4928: Paid $2,450.00", key="hmac_msg_in")
            hmac_key = st.text_input("Shared Secret Key", value="CorporateSecretToken_2026", type="password", key="hmac_key_in")
            if st.button("Generate HMAC", key="btn_gen_hmac"):
                if not hmac_msg.strip() or not hmac_key:
                    st.warning("⚠️ Both message and secret key are required.")
                else:
                    try:
                        code = hashing.generate_hmac(hmac_msg, hmac_key)
                        st.success("✅ HMAC-SHA256 Digest:")
                        st.code(code, language="text")
                    except Exception as e:
                        st.error(f"❌ HMAC Generation Error: {str(e)}")

        with col_h2:
            st.subheader("Verify HMAC")
            v_msg = st.text_area("Message to Verify", value="Invoice #4928: Paid $2,450.00", key="v_hmac_msg")
            v_code = st.text_input("Expected HMAC Digest", placeholder="Paste 64-char HMAC digest...", key="v_hmac_code")
            v_key = st.text_input("Shared Secret Key", type="password", key="v_hmac_key")

            if st.button("Verify HMAC", key="btn_verify_hmac"):
                if not v_msg.strip() or not v_code.strip() or not v_key:
                    st.warning("⚠️ All fields are required for verification.")
                else:
                    try:
                        valid = hashing.verify_hmac(v_msg, v_key, v_code)
                        if valid:
                            st.success("✅ HMAC VALID! Authenticity and integrity confirmed.")
                        else:
                            st.error("❌ HMAC INVALID! Authentication failed.")
                    except Exception as e:
                        st.error(f"❌ Verification Error: {str(e)}")


# =====================================================================
# PAGE 6: FILE INTEGRITY CHECKER
# =====================================================================
def page_file_integrity():
    st.title("🔍 File Integrity Checker")
    st.caption("Verify file authenticity by comparing checksums with automated algorithm detection.")

    integrity_file = st.file_uploader("Upload File to Verify", key="integrity_uploader")
    expected_hash = st.text_input("Expected Checksum / Hash", placeholder="Paste expected hash (MD5, SHA-1, SHA-256, or SHA-512)...", key="expected_hash_in")

    if st.button("Verify File Integrity", type="primary"):
        if not integrity_file:
            st.warning("⚠️ Please upload a file to check.")
            return
        if not expected_hash.strip():
            st.warning("⚠️ Please paste the expected hash checksum.")
            return

        try:
            with st.spinner("Streaming file in 8 KB chunks & checking integrity..."):
                match, actual_hash, algo = hashing.compare_hash(integrity_file, expected_hash)

            st.markdown(f"**Detected Algorithm**: `{algo}` (based on hash length: {len(expected_hash.strip())} hex characters)")

            if match:
                st.success("### ✅ INTEGRITY VERIFIED: MATCH!")
                st.markdown("The uploaded file exactly matches the expected cryptographic checksum. No tampering detected.")
            else:
                st.error("### ❌ INTEGRITY COMPROMISED: MISMATCH!")
                st.markdown("The computed hash does not match the expected hash. The file may be corrupt or tampered with.")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Expected Hash:**")
                st.code(expected_hash.strip().lower(), language="text")
            with col2:
                st.markdown("**Actual Computed Hash:**")
                st.code(actual_hash, language="text")

        except ValueError as e:
            st.error(f"❌ Input Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error during integrity check: {str(e)}")


# =====================================================================
# PAGE 7: PASSWORD TOOLS
# =====================================================================
def page_password_tools():
    st.title("🎲 Password Tools")
    st.caption("Password strength evaluation, Shannon entropy estimation, and cryptographically secure generation.")

    tab_eval, tab_gen = st.tabs(["🛡️ Strength Evaluator", "⚡ Secure Password Generator"])

    with tab_eval:
        st.subheader("Password Strength & Entropy Analyzer")
        pwd_input = st.text_input("Enter Password to Test", type="password", key="pwd_eval_in")

        if pwd_input:
            eval_res = password_tools.check_password_strength(pwd_input)

            # Progress Bar and Label
            pct = eval_res["percentage"]
            label = eval_res["label"]

            color_map = {
                "Weak": "#EF4444",
                "Fair": "#F59E0B",
                "Strong": "#10B981",
                "Very Strong": "#3B82F6",
            }
            color = color_map.get(label, "#9CA3AF")

            st.markdown(f"**Strength Score:** <span style='color:{color}; font-size:1.3rem; font-weight:bold;'>{label}</span>", unsafe_allow_html=True)
            st.progress(pct)

            col1, col2, col3 = st.columns(3)
            col1.metric("Entropy", f"{eval_res['entropy_bits']} bits")
            col2.metric("Length", len(pwd_input))
            col3.metric("Common Weak Word?", "Yes ⚠️" if eval_res["common_match"] else "No ✅")

            st.markdown("#### Improvement Recommendations:")
            for tip in eval_res["tips"]:
                st.markdown(f"- {tip}")

    with tab_gen:
        st.subheader("Cryptographically Secure Password Generator")
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            gen_len = st.slider("Password Length", min_value=8, max_value=64, value=16, step=1)
            inc_upper = st.checkbox("Include Uppercase (A-Z)", value=True)
            inc_lower = st.checkbox("Include Lowercase (a-z)", value=True)
            inc_digits = st.checkbox("Include Digits (0-9)", value=True)
            inc_symbols = st.checkbox("Include Symbols (!@#$%)", value=True)

        with col_g2:
            if st.button("Generate Secure Password", type="primary"):
                try:
                    new_pwd = password_tools.generate_password(
                        length=gen_len,
                        include_upper=inc_upper,
                        include_lower=inc_lower,
                        include_digits=inc_digits,
                        include_symbols=inc_symbols,
                    )
                    st.success("✅ Generated Password (CSPRNG):")
                    st.code(new_pwd, language="text")

                    # Immediate strength evaluation
                    gen_eval = password_tools.check_password_strength(new_pwd)
                    st.caption(f"Estimated Entropy: **{gen_eval['entropy_bits']} bits** | Strength: **{gen_eval['label']}**")
                except ValueError as e:
                    st.error(f"❌ {str(e)}")


# =====================================================================
# PAGE 8: FREQUENCY ANALYSIS
# =====================================================================
def page_frequency_analysis():
    st.title("📊 Letter Frequency Analysis")
    st.caption("Cryptanalysis of monoalphabetic ciphers using statistical frequency distributions.")

    with st.expander("ℹ️ How Frequency Analysis Breaks Classical Ciphers", expanded=False):
        st.markdown(
            """
            In natural English text, letters do not appear with equal probability:
            - **E** is the most frequent (~12.7%), followed by **T** (~9.1%), **A** (~8.2%), and **O** (~7.5%).
            - **Z, Q, X, J** are the rarest (< 0.2%).
            
            **Monoalphabetic substitution ciphers** (like Caesar, Affine, and Atbash) preserve these frequency patterns,
            simply shifting or substituting the letters. By analyzing the frequencies of letters in the ciphertext,
            a cryptanalyst can map high-frequency ciphertext letters to standard English letters to crack the key!
            """
        )

    default_sample = (
        "UZSO ROVUBGIW SOWFOHFFW QOFUBGHDW QOB WFFW QOFUBGHDW "
        "INFORMATION SECURITY AND CRYPTOGRAPHY STUDY FOR NETWORK PROTECTION "
        "CLASSICAL SUBSTITUTION CIPHERS LEAK STATISTICAL PATTERNS THROUGH LETTER COUNTS"
    )

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("Load Sample Text"):
            st.session_state.freq_input = default_sample

    input_text = st.text_area(
        "Enter Plaintext or Ciphertext for Analysis",
        value=st.session_state.get("freq_input", default_sample),
        height=140,
    )

    if input_text.strip():
        result = analysis.analyze_frequency(input_text)
        df_freq = pd.DataFrame(result["data_rows"])

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Letters Counted", result["total_letters"])
        most_freq = max(result["letter_counts"], key=result["letter_counts"].get) if result["total_letters"] > 0 else "N/A"
        col_m2.metric("Most Frequent Letter", f"{most_freq} ({result['letter_counts'].get(most_freq, 0)} times)")
        col_m3.metric("Observed / Alphabet Size", f"{sum(1 for cnt in result['letter_counts'].values() if cnt > 0)} / 26")

        st.subheader("Observed Frequency vs. Standard English Benchmark")
        # Plot bar chart with Letter as index
        chart_df = df_freq.set_index("Letter")[["Percentage", "English Standard (%)"]]
        st.bar_chart(chart_df)

        with st.expander("📋 Detailed Frequency Table"):
            st.dataframe(df_freq, use_container_width=True)


# =====================================================================
# MAIN ROUTING & FOOTER
# =====================================================================
def main():
    page = render_sidebar()

    if page == "🏠 Home / About":
        page_home()
    elif page == "📜 Classical Ciphers":
        page_classical_ciphers()
    elif page == "🛡️ AES Encryption":
        page_aes_encryption()
    elif page == "🔑 RSA & Digital Signatures":
        page_rsa()
    elif page == "⚡ Hashing & HMAC":
        page_hashing()
    elif page == "🔍 File Integrity Checker":
        page_file_integrity()
    elif page == "🎲 Password Tools":
        page_password_tools()
    elif page == "📊 Frequency Analysis":
        page_frequency_analysis()

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>"
        "🔐 <b>CipherLab</b> — Information & Network Security Mini Project &bull; Built with Python & Streamlit &bull; "
        "Strictly for educational and research purposes."
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
