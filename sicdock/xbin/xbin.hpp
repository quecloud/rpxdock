#pragma once

#include "sicdock/geom/bcc.hpp"
#include "sicdock/util/numeric.hpp"
#include "sicdock/util/types.hpp"
// #include "util/assert.hpp"
// #include "util/dilated_int.hpp"

// #include <boost/utility/binary.hpp>

namespace sicdock {
namespace xbin {

using namespace util;

// TODO: add bounds check angles version!

template <typename _Xform, typename _K = uint64_t>
struct XformHash_bt24_BCC6 {
  using Xform = _Xform;
  using K = _K;
  typedef typename Xform::Scalar F;
  typedef typename Xform::Scalar Scalar;
  typedef sicdock::geom::BCC<6, F, K> Grid;
  typedef Eigen::Array<F, 6, 1> F6;
  typedef Eigen::Array<K, 6, 1> I6;

  F grid_size_ = -1;
  F grid_spacing_ = -1;
  Grid grid6_;
  auto grid() const { return grid6_; }
  F cart_resl_ = -1, ori_resl_ = -1, cart_bound_ = -1;
  F cart_resl() const { return cart_resl_; }
  F ori_resl() const { return ori_resl_; }
  F cart_bound() const { return cart_bound_; }
  int ori_nside_ = -1;
  int ori_nside() const { return ori_nside_; }

  static std::string name() { return "XformHash_bt24_BCC6"; }

  XformHash_bt24_BCC6() {}
  template <typename Float>
  XformHash_bt24_BCC6(Float cart_resl, Float ori_resl,
                      Float cart_bound = 512.0) {
    this->cart_bound_ = cart_bound;
    init(cart_resl, ori_resl, cart_bound);
  }
  XformHash_bt24_BCC6(F cart_resl, int ori_nside, F cart_bound) {
    ori_resl_ = get_ori_resl(ori_nside);
    init2(cart_resl, ori_nside, cart_bound);
  }
  int get_ori_nside() {
    int ori_nside = 1;
    while (covrad_[ori_nside - 1] > ori_resl_ && ori_nside < 30) ++ori_nside;
    ori_resl_ = get_ori_resl(ori_nside);
    return ori_nside;
  }
  F get_ori_resl(int nside) { return covrad_[nside - 1]; }
  void init(F cart_resl, F ori_resl, F cart_bound = 512.0) {
    this->cart_bound_ = cart_bound;
    this->ori_resl_ = ori_resl;
    init2(cart_resl, get_ori_nside(), cart_bound);
  }
  void init2(F cart_resl, int ori_nside, F cart_bound) {
    cart_resl_ = cart_resl / (sqrt(3.0) / 2.0);
    cart_bound_ = cart_bound;
    ori_nside_ = ori_nside;
    F6 lb, ub;
    I6 nside = get_bounds(cart_resl_, ori_nside_, cart_bound_, lb, ub);
    grid6_.init(nside, lb, ub);
  }
  I6 get_bounds(F cart_resl, int ori_nside, float cart_bound, F6 &lb, F6 &ub) {
    I6 nside;
    if (2 * (int)(cart_bound / cart_resl) > 8192) {
      throw std::out_of_range("can have at most 8192 cart cells!");
    }
    nside[0] = nside[1] = nside[2] = 2.0 * cart_bound / cart_resl;
    nside[3] = nside[4] = nside[5] = ori_nside + 1;
    lb[0] = lb[1] = lb[2] = -cart_bound;
    ub[0] = ub[1] = ub[2] = cart_bound;
    lb[3] = lb[4] = lb[5] = -1.0 / ori_nside;
    ub[3] = ub[4] = ub[5] = 1.0;
    return nside;
  }
  F6 xform_to_F6(Xform x, K &cell_index) const {
    Eigen::Matrix<F, 3, 3> rotation = x.linear();
    Eigen::Quaternion<F> q(rotation);
    // std::cout << q.coeffs().transpose() << std::endl;
    get_cell_48cell_half(q.coeffs(), cell_index);
    q = hbt24_cellcen<F>(cell_index).inverse() * q;
    assert(cell_index < 24);
    q = to_half_cell(q);
    F w = 2 * (sqrt(2) - 1);
    F a = q.x() / q.w() / w + 0.5;
    F b = q.y() / q.w() / w + 0.5;
    F c = q.z() / q.w() / w + 0.5;
    a = fmin(1, fmax(0, a));
    b = fmin(1, fmax(0, b));
    c = fmin(1, fmax(0, c));
    F6 params6;
    for (int i = 0; i < 3; ++i) params6[i] = x.translation()[i];
    params6[3] = a;
    params6[4] = b;
    params6[5] = c;
    // std::cout << params6 << std::endl;
    return params6;
  }
  Xform F6_to_xform(F6 params6, K cell_index) const {
    F w = 2 * (sqrt(2) - 1);
    // F3 params(params6[3], params6[4], params6[5]);
    // clamp01<3>(params);
    // params = w * (params - 0.5);  // now |params| < sqrt(2)-1
    // Eigen::Quaternion<F> q(1.0, params[0], params[1], params[2]);
    Eigen::Quaternion<F> q(1.0, w * (fmin(1.0, fmax(0.0, params6[3])) - 0.5),
                           w * (fmin(1.0, fmax(0.0, params6[4])) - 0.5),
                           w * (fmin(1.0, fmax(0.0, params6[5])) - 0.5));

    q.normalize();
    q = hbt24_cellcen<F>(cell_index) * q;
    Xform center(q.matrix());
    for (int i = 0; i < 3; ++i) center.translation()[i] = params6[i];
    return center;
  }

  K get_key(Xform x) const {
    K cell_index;
    F6 p6 = xform_to_F6(x, cell_index);
#ifdef NDEBUG
#undef NDEBUG
    assert((grid6_[p6] >> 55) == 0);
#define NDEBUG
#else
    assert((grid6_[p6] >> 55) == 0);
#endif

    return combine_cell_grid_index(cell_index, grid6_[p6]);
  }
  K cell_index(K key) const { return key >> 55; }
  K combine_cell_grid_index(K cell_index, K grid_index) const {
    return cell_index << 55 | grid_index;
  }
  Xform get_center(K key) const {
    K cell_index = key >> 55;
    auto tmp = grid6_[key & (((K)1 << 55) - (K)1)];
    F6 params6;
    for (int i = 0; i < 6; ++i) params6[i] = tmp[i];
    return F6_to_xform(params6, cell_index);
  }
  K approx_size() const { return grid6_.size() * 24; }
  K approx_nori() const {
    static int const nori[18] = {192,   648,   1521,  2855,   4990,   7917,
                                 11682, 16693, 23011, 30471,  39504,  50464,
                                 62849, 77169, 93903, 112604, 133352, 157103};
    return nori[grid6_.nside_[3] - 2];  // -1 for 0-index, -1 for ori_side+1
  }

  Grid grid6() const { return grid6_; }

  constexpr static float const covrad_[30] = {
      68.01665538755952,   // 1
      37.609910622634885,  // 2
      25.161985041078903,  // 3
      19.234712994263397,  // 4
      15.051679420273125,  // 5
      12.673170024876562,  // 6
      10.910165052027457,  // 7
      9.56595406234607,    // 8
      8.385222483324211,   // 9
      7.608106253859658,   // 10
      6.967540100300543,   // 11
      6.322115851799134,   // 12
      5.914757505612797,   // 13
      5.4567262070302025,  // 14
      5.09134727351595,    // 15
      4.686447098346156,   // 16
      4.487953966250555,   // 17
      4.261457587347119,   // 18
      4.090645267179167,   // 19
      3.7881921869273563,  // 20
      3.586942657822621,   // 21
      3.4407192960024973,  // 22
      3.3028933870146857,  // 23
      3.233183894633594,   // 24
      3.104387238338871,   // 25
      2.944661982283254,   // 26
      2.830655160174503,   // 27
      2.78906624167323,    // 28
      2.624501847820492,   // 29
  };
};

}  // namespace xbin
}  // namespace sicdock
