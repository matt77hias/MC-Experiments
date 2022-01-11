[![License][s1]][li]

[s1]: https://img.shields.io/badge/licence-GPL%203.0-blue.svg
[li]: https://raw.githubusercontent.com/matt77hias/MCExperiments/master/LICENSE.txt

# MC-Experiments

Teaching: Monte Carlo Integration Techniques

## About
Some Monte Carlo experiments used for teaching Monte Carlo Integration Techniques for the course *Problem Solving and Design: Part 3* (1st Semester - 2nd Bachelor of Science in Engineering).

## Use

### Basics

#### The effect of increasing the number of samples
<p align="center">
<img src="res/RMSE_f_n3.png" width="285">
</p>

#### The effect of increasing the dimensionality
<p align="center">
<img src="res/RMSE_f_n2.png" width="273">
<img src="res/RMSE_f_n3.png" width="273">
<img src="res/RMSE_f_n10.png" width="273">
</p>

#### The effect of increasing the domain
<p align="center">
<img src="res/RMSE_f_n3.png" width="273">
<img src="res/RMSE_f_w4.png" width="273">
<img src="res/RMSE_f_w8.png" width="273">
</p>

```python
# Code
test.test_session1()
```

### Sampling strategies

#### Monte Carlo sampling strategies
<p align="center">
<img src="res/RMSE_f_hm.png" width="273">
<img src="res/RMSE_f_u.png" width="273">
<img src="res/RMSE_f_s.png" width="273">
</p>

#### Quasi Monte Carlo sampling strategies
<p align="center">
<img src="res/RMSE_f_h.png" width="273">
</p>

```python
# Code
test.test_session2(a=3, n=3)
```
