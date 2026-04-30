
$$R = R_z(\gamma) \cdot R_y(\beta) \cdot R_x(\alpha)$$

$$R_x(\alpha) = \begin{pmatrix}
1 & 0 & 0 \\
0 & \cos\alpha & -\sin\alpha \\
0 & \sin\alpha & \cos\alpha
\end{pmatrix}$$

$$R_y(\beta) = \begin{pmatrix}
\cos\beta & 0 & \sin\beta \\
0 & 1 & 0 \\
-\sin\beta & 0 & \cos\beta
\end{pmatrix}$$

$$R_z(\gamma) = \begin{pmatrix}
\cos\gamma & -\sin\gamma & 0 \\
\sin\gamma & \cos\gamma & 0 \\
0 & 0 & 1
\end{pmatrix}$$

$$R_y(\beta)R_x(\alpha)= \begin{pmatrix}
\cos\beta & 0 & \sin\beta \\
0 & 1 & 0 \\
-\sin\beta & 0 & \cos\beta
\end{pmatrix}
\begin{pmatrix}
1 & 0 & 0 \\
0 & \cos\alpha & -\sin\alpha \\
0 & \sin\alpha & \cos\alpha
\end{pmatrix}$$

$$R_y(\beta)R_x(\alpha)= \begin{pmatrix}
\cos\beta & \sin\beta\sin\alpha & \sin\beta\cos\alpha \\
0 & \cos\alpha & -\sin\alpha \\
-\sin\beta & \cos\beta\sin\alpha & \cos\beta\cos\alpha
\end{pmatrix}$$

$$R = R_z(\gamma)
\left(
R_y(\beta)R_x(\alpha)
\right)$$

$$R =
\begin{pmatrix}
\cos\gamma & -\sin\gamma & 0 \\
\sin\gamma & \cos\gamma & 0 \\
0 & 0 & 1
\end{pmatrix}
\begin{pmatrix}
\cos\beta & \sin\beta\sin\alpha & \sin\beta\cos\alpha \\
0 & \cos\alpha & -\sin\alpha \\
-\sin\beta & \cos\beta\sin\alpha & \cos\beta\cos\alpha
\end{pmatrix}$$

$$R =
\begin{pmatrix}
\cos\gamma\cos\beta
&
\cos\gamma\sin\beta\sin\alpha - \sin\gamma\cos\alpha
&
\cos\gamma\sin\beta\cos\alpha + \sin\gamma\sin\alpha
\\
\sin\gamma\cos\beta
&
\sin\gamma\sin\beta\sin\alpha + \cos\gamma\cos\alpha
&
\sin\gamma\sin\beta\cos\alpha - \cos\gamma\sin\alpha
\\
-\sin\beta
&
\cos\beta\sin\alpha
&
\cos\beta\cos\alpha
\end{pmatrix}$$

$$\beta = 90^\circ = \frac{\pi}{2}$$

$$\sin\beta = 1$$

$$\cos\beta = 0$$

$$R =
\begin{pmatrix}
\cos\gamma \cdot 0
&
\cos\gamma \cdot 1 \cdot \sin\alpha - \sin\gamma\cos\alpha
&
\cos\gamma \cdot 1 \cdot \cos\alpha + \sin\gamma\sin\alpha
\\
\sin\gamma \cdot 0
&
\sin\gamma \cdot 1 \cdot \sin\alpha + \cos\gamma\cos\alpha
&
\sin\gamma \cdot 1 \cdot \cos\alpha - \cos\gamma\sin\alpha
\\
-1
&
0 \cdot \sin\alpha
&
0 \cdot \cos\alpha
\end{pmatrix}$$

$$R =
\begin{pmatrix}
0
&
\cos\gamma\sin\alpha - \sin\gamma\cos\alpha
&
\cos\gamma\cos\alpha + \sin\gamma\sin\alpha
\\
0
&
\sin\gamma\sin\alpha + \cos\gamma\cos\alpha
&
\sin\gamma\cos\alpha - \cos\gamma\sin\alpha
\\
-1
&
0
&
0
\end{pmatrix}$$

$$\sin(\alpha - \gamma)= \sin\alpha\cos\gamma - \cos\alpha\sin\gamma$$

$$\cos(\alpha - \gamma)
=\cos\alpha\cos\gamma + \sin\alpha\sin\gamma$$

$$R = \begin{pmatrix} 0 & \sin(\alpha - \gamma)& \cos(\alpha - \gamma)\\ 0 & \cos(\alpha - \gamma)& -\sin(\alpha - \gamma)\\ -1 & 0 & 0 \end{pmatrix}$$
з фінальної матриці наглядно видно що результат залежить від $\alpha - \gamma$